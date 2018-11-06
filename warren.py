from stnpool import StnPool
import numpy as np
import copy
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from operation import Operation
from titulo import Titulo, TipoTitulo
import time
import math
from datetime import datetime, timedelta
import pandas as pd
from sklearn.linear_model import LinearRegression

class Warren():

	def __init__(self):
		self._stnpool = StnPool()
		self._titulos_ativos = None
		self._array_titulos = {}
		self._data_plot = {}

		self._data_final = datetime.now()
		self._data_inicial = self._data_final + timedelta(days=-300)

		self._offset_janela = 10
		self._limite_superior_janela = self._data_inicial + timedelta(days=self._offset_janela)
		self._limite_inferior_janela = self._data_inicial
		self._janela_taxas = []
		self._janela_datas = []

		self._trend_lines = []
		self._coefficients = None

		self._MM_WINDOW_SHORT = 2
		self._MM_WINDOW_LONG = 30

		self._meta_rendimento = 0.02 # 10%
		self._saldo_disponivel = 50000.00 # R$ 50.000,00 Reais
		self._valor_operacao = self._saldo_disponivel * 0.05 # 25% do Capital Inicial
		self._minhas_operacoes = None

		self._historico_operacoes = []

		self._minimo_global = [999, None]
		self._maximo_global = [0, None]
		self._minino_local = [999, None]
		self._maximo_local = [0, None]

	def processarDados(self):
		# Títulos Ativos
		self._titulos_ativos = self._stnpool.getTitulosAtivos()

		# Iniciar Dict Dados
		for key_compra_venda, values_tipo_vencimento in self._titulos_ativos.items():
			for key_tipo, values_vencimento in values_tipo_vencimento.items():
				self._data_plot[key_tipo] = {}
				for vencimento in values_vencimento:
					self._data_plot[key_tipo][vencimento] = {
						'titulos' : [], 'taxas_compra' : [], 'taxas_venda' : [], 'datas' : [] }

		# Processar Dados dos Títulos
		historico_titulos = self._stnpool.getHistoricoTitulos()

		for titulo in historico_titulos:
			tipo = titulo.getTt()
			vencimento = titulo.getDv()
			data = titulo.getDb()
			taxa_compra = titulo.getTc()
			taxa_venda = titulo.getTv()

			if tipo in self._data_plot and data > self._data_inicial and vencimento in self._data_plot[tipo]:
				self._data_plot[tipo][vencimento]['titulos'].append(titulo)
				self._data_plot[tipo][vencimento]['taxas_compra'].append(taxa_compra)
				self._data_plot[tipo][vencimento]['taxas_venda'].append(taxa_venda)
				self._data_plot[tipo][vencimento]['datas'].append(data)

	def simular(self, tipo, vencimento):
		self._minhas_operacoes = []

		titulos = self.select(tipo, vencimento)

		s = pd.Series(titulos['taxas_compra'])

		titulos['mm_short'] = s.rolling(self._MM_WINDOW_SHORT).mean().tolist()
		titulos['mm_long'] = s.rolling(self._MM_WINDOW_LONG).mean().tolist()

		P1 = [1 if (titulos['taxas_compra'][0] - titulos['mm_short'][0]) >= 0 else -1, None, None]
		P2 = copy.copy(P1)
		
		for i in range(len(titulos['titulos'])):
			s_titulo = titulos['titulos'][i]
			s_tx_compra = titulos['taxas_compra'][i]
			s_tx_venda = titulos['taxas_venda'][i]
			s_data = titulos['datas'][i]
			s_mm_short = titulos['mm_short'][i]
			s_mm_long = titulos['mm_long'][i]
			s_preco_compra, s_preco_venda = s_titulo.getPu()

			# Atualizar máximos e mínimos
			if self._minimo_global[0] > s_tx_compra:
				self._minimo_global = [s_tx_compra, s_data]

			if self._maximo_global[0] < s_tx_compra:
				self._maximo_global = [s_tx_compra, s_data]

			if s_data >= self._limite_inferior_janela and s_data <= self._limite_superior_janela:
				if self._minino_local[0] > s_tx_compra:
					self._minino_local = [s_tx_compra, s_data]

				if self._maximo_local[0] < s_tx_compra:
					self._maximo_local = [s_tx_compra, s_data]

				self._janela_taxas.append(s_tx_compra)
				self._janela_datas.append(s_data)

			else:
				self._limite_inferior_janela = self._limite_superior_janela
				self._limite_superior_janela = self._limite_superior_janela + timedelta(days=self._offset_janela)
				self._minimo_local = [s_tx_compra, s_data]
				self._maximo_local = [s_tx_compra, s_data]
				self._coefficients, residuals, _, _, _ = np.polyfit(range(2), [self._janela_taxas[0], self._janela_taxas[-1]],1,full=True)
				self._trend_lines.append([[self._janela_datas[0], self._janela_datas[-1]], [self._janela_taxas[0], self._janela_taxas[-1]], self._coefficients])
				self._janela_taxas = [s_tx_compra]
				self._janela_datas = [s_data]

			if P1[0] * P2[0] <= 0 and not math.isnan(s_mm_short) and len(self._trend_lines) > 0:	
				# Mudança de + para -
				if P2[0] > 0 and self._trend_lines[-1][2][0] > 0 and s_tx_compra > self._maximo_local[0] * 0.95:
					# Compra
					valor_minimo = s_titulo.getVm()

					qnt = int(self._valor_operacao / valor_minimo) * valor_minimo

					if self._saldo_disponivel > 0 and self._saldo_disponivel > qnt:
						self._minhas_operacoes.append(Operation(s_titulo, 'compra', qnt))
						self._saldo_disponivel -= qnt
						self._historico_operacoes.append([s_data, s_tx_compra, 'compra'])
						print("COMPRA ", s_data, s_tx_compra, qnt, self._saldo_disponivel)

				# Mudança de - para +
				else:
					if self._trend_lines[-1][2][0] < 0 and len(self._minhas_operacoes) > 0:
						# Vende se Lucro superar lucro meta
						rendimento = 0
						for o in self._minhas_operacoes:
							rendimento += o.calculaRendimentoMensal(s_preco_venda, s_titulo.getDb())

						if rendimento / len(self._minhas_operacoes) > self._meta_rendimento:
							#print("Venda de Oportunidade")
							for o in self._minhas_operacoes:
								# Venda
								self._saldo_disponivel += o.resgatar(s_preco_venda, s_titulo.getDb())
								self._historico_operacoes.append([s_data, s_tx_venda, 'venda'])
								print("VENDA ", s_data, s_tx_compra, o.calculaRendimentoMensal(s_preco_venda, s_titulo.getDb()), self._saldo_disponivel)
								
							self._minhas_operacoes = []

			P1 = [P2[0], P2[1], P2[2]]
			P2 = [1 if (s_tx_compra - s_mm_short) >= 0 else -1, s_titulo.getTc(), s_titulo.getDb()]

		# Zeragem
		print("Zeragem")
		s_preco_compra, s_preco_venda = titulos['titulos'][-1].getPu()

		for o in self._minhas_operacoes:
			# Venda
			self._saldo_disponivel += o.resgatar(s_preco_venda, s_titulo.getDb())
			self._historico_operacoes.append([titulos['datas'][i], titulos['taxas_compra'][i], 'venda'])
			self._minhas_operacoes = []
			print("VENDA ", titulos['datas'][i], o.calculaRendimentoTotal(s_preco_venda, s_titulo.getDb()), self._saldo_disponivel)

		print(self._saldo_disponivel)
		
		self.plot(tipo, vencimento)

	def plot(self, tipo, vencimento):
		years = mdates.MonthLocator()
		months = mdates.DayLocator()
		yearsFmt = mdates.DateFormatter('%d-%m-%Y')

		fig, ax = plt.subplots()

		taxas = 'taxas_compra'

		for key_tipo, values_tipo in self._data_plot.items():
			if tipo == key_tipo:
				for key_vencimento, values_vencimento in values_tipo.items():
					if key_vencimento == vencimento:
						label = key_tipo + " " + str(key_vencimento.year)
						plt.xticks(rotation=70)
						ax.plot(values_vencimento['datas'], values_vencimento[taxas], label=label)
						#s = pd.Series(values_vencimento[taxas])
						#ax.plot(values_vencimento['datas'], s.rolling(self._MM_WINDOW_SHORT).mean().tolist(), label=label + " MM")
						#ax.plot(values_vencimento['datas'], s.rolling(self._MM_WINDOW_LONG).mean().tolist(), label=label + " MM")

			# format the ticks
			ax.xaxis.set_major_locator(years)
			ax.xaxis.set_major_formatter(yearsFmt)
			ax.xaxis.set_minor_locator(months)

			#ax.set_facecolor('xkcd:black')

			# round to nearest years...
			datemin = np.datetime64(self._data_inicial, 'M')
			datemax = np.datetime64(self._data_final, 'M') + np.timedelta64(1, 'M')
			ax.set_xlim(datemin, datemax)

			ax.format_xdata = mdates.DateFormatter('%d/%m/%Y')

		for o in self._historico_operacoes:
			color = "Red" if o[2] == 'compra' else "Green"
			ax.scatter([o[0]],[o[1]], s=40, edgecolor=color, facecolor=color, linewidth=1)
		
		# Plot Mínimo e Máximo Globais
		#ax.scatter([self._maximo_global[1]],[self._maximo_global[0]], s=40, edgecolor=color, facecolor=color, linewidth=1)
		#ax.scatter([self._minimo_global[1]],[self._minimo_global[0]], s=40, edgecolor=color, facecolor=color, linewidth=1)

		for trend_line in self._trend_lines:
			ax.plot(trend_line[0], [trend_line[2][0]*x + trend_line[2][1] for x in range(len(trend_line[0]))], color= "black")
			
		plt.legend()
		plt.show()

	def select(self, tipo, vencimento):
		for key_tipo, values_tipo in self._data_plot.items():
			if tipo == key_tipo:
				for key_vencimento, values_vencimento in values_tipo.items():
					if key_vencimento == vencimento:
						return values_vencimento

if __name__ == "__main__":
	warren = Warren()
	warren.processarDados()
	warren.simular(TipoTitulo.IPCA.value, datetime.strptime('15/05/2035', '%d/%m/%Y'))
	#warren.simular(TipoTitulo.PRE.value, datetime.strptime('01/01/2021', '%d/%m/%Y'))