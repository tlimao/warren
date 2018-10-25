import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import time
from titulo import TipoTitulo
from stnpool import StnPool
from datetime import datetime, timedelta

class StnEstatisticas():

	def __init__(self):
		self._stnpool = StnPool()
		self._stnpool.start()
		time.sleep(40)

		self._titulos_ativos = self._stnpool.getTitulosAtivos()
		self._array_titulos = {}

		self._data_plot = {}
		self._MmL = []
		self._MmE = []

		self._data_final = datetime.now()
		self._data_inicial = self._data_final + timedelta(days=-200)

		self._MM_WINDOW_SHORT = 2
		self._MM_WINDOW_LONG = 15

	def processData(self):
		# Iniciar Dict Dados
		for key_compra_venda, values_tipo_vencimento in self._titulos_ativos.items():
			self._data_plot[key_compra_venda] = {}
			for key_tipo, values_vencimento in values_tipo_vencimento.items():
				self._data_plot[key_compra_venda][key_tipo] = {}
				for vencimento in values_vencimento:
					self._data_plot[key_compra_venda][key_tipo][vencimento] = {
						'titulos' : [], 'taxas' : [], 'datas' : [] }

		# Processar Dados de Compra
		titulos_compra = self._stnpool.getHistoricoTitulosCompra()
		for titulo in titulos_compra:
			tipo = titulo.getTt() + " " + str(titulo.getDv().year)
			vencimento = titulo.getDv()
			data = titulo.getDb()
			taxa = titulo.getTc()
			if tipo in self._titulos_ativos['compra'] and data > self._data_inicial:
				self._data_plot['compra'][tipo][vencimento]['titulos'].append(titulo)
				self._data_plot['compra'][tipo][vencimento]['taxas'].append(taxa)
				self._data_plot['compra'][tipo][vencimento]['datas'].append(data)

		# Processar Dados de Venda
		titulos_venda = self._stnpool.getHistoricoTitulosVenda()
		for titulo in titulos_venda:
			tipo = titulo.getTt() + " " + str(titulo.getDv().year)
			vencimento = titulo.getDv()
			data = titulo.getDb()
			taxa = titulo.getTv()
			if tipo in self._titulos_ativos['venda'] and data > self._data_inicial:
				self._data_plot['venda'][tipo][vencimento]['titulos'].append(titulo)
				self._data_plot['venda'][tipo][vencimento]['taxas'].append(taxa)
				self._data_plot['venda'][tipo][vencimento]['datas'].append(data)

	def getMmL(self):
		pass

	def getMmE(self):
		pass

	def plot(self, tipo, compraVenda, vencimento):
		years = mdates.MonthLocator()
		months = mdates.DayLocator()
		yearsFmt = mdates.DateFormatter('%d-%m-%Y')

		fig, ax = plt.subplots()

		for key_tipo, values_tipo in self._data_plot[compraVenda].items():
			if tipo in key_tipo:
				for key_vencimento, values_vencimento in values_tipo.items():
					if key_vencimento.year >= vencimento.year:
						ax.plot(values_vencimento['datas'], values_vencimento['taxas'], label=key_tipo)
						s = pd.Series(values_vencimento['taxas'])
						ax.plot(values_vencimento['datas'], s.rolling(self._MM_WINDOW_SHORT).mean().tolist(), label=str(key_tipo) + " MM")
						ax.plot(values_vencimento['datas'], s.rolling(self._MM_WINDOW_LONG).mean().tolist(), label=str(key_tipo) + " MM")

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

		plt.legend()
		plt.show()

if __name__ == '__main__':
	estatisticas = StnEstatisticas()
	estatisticas.processData()
	estatisticas.plot(TipoTitulo.PRE.value, 'compra', datetime.strptime('01/01/2026', '%d/%m/%Y'))