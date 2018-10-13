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
		time.sleep(20)
		self._titulos_ativos = self._stnpool.getTitulosAtivos()

		self._array_titulos = {}
		self._MmL = []
		self._MmE = []

		self._data_final = datetime.now()
		self._data_inicial = self._data_final + timedelta(days=-900)

		self._MM_WINDOW_SHORT = 2
		self._MM_WINDOW_LONG = 15

		self._initArrayTitulos()

	def processData(self):
		titulos = self._stnpool.getHistoricoTitulos()
		titulos_hoje = self._stnpool.getTitulos()

		for titulo in titulos:
			tipo = titulo.getTt().upper()
			vencimento = titulo.getDv()
			dataBase = titulo.getDb()

			if vencimento > self._data_final and dataBase > self._data_inicial:
				if TipoTitulo.IPCA.value in tipo:
					self._array_titulos[TipoTitulo.IPCA.value].append(titulo)
				elif TipoTitulo.PRE.value in tipo:
					self._array_titulos[TipoTitulo.PRE.value].append(titulo)

		#for titulo in titulos_hoje:
		#	tipo = titulo.getTt().upper()
		#	vencimento = titulo.getDv()
		#	dataBase = titulo.getDb()

		#	if TipoTitulo.IPCA.value in tipo:
		#		self._array_titulos[TipoTitulo.IPCA.value].append(titulo)
		#	elif TipoTitulo.PRE.value in tipo:
		#		self._array_titulos[TipoTitulo.PRE.value].append(titulo)

	def _initArrayTitulos(self):
		for tipo in list(TipoTitulo):
			self._array_titulos[tipo.value] = []

	def getMmL(self):
		pass

	def getMmE(self):
		pass

	def plot(self, tipo, compraVenda, vencimento):
		data_plot = {}

		for t in self._array_titulos[tipo]:
			tipo_titulo = t.getTt().upper()
			data_vencimento = t.getDv()
			if tipo in tipo_titulo and data_vencimento >= vencimento:
				if compraVenda == 'compra' and t.isCompra() and \
					(tipo_titulo + " " + str(data_vencimento.year)) in self._titulos_ativos['compra']:
					if tipo_titulo not in data_plot:
						data_plot[tipo_titulo] = { str(data_vencimento) : [[], []] }

					if str(data_vencimento) not in data_plot[tipo_titulo]:
						data_plot[tipo_titulo][str(data_vencimento)] = [[], []]

					data_plot[tipo_titulo][str(data_vencimento)][0].append(t.getTc())
					data_plot[tipo_titulo][str(data_vencimento)][1].append(t.getDb())

				elif compraVenda == 'venda' and t.isVenda() and \
					(tipo_titulo + " " + str(data_vencimento.year)) in self._titulos_ativos['venda']:
					y_taxas.append(t.getTv())
					x_datas.append(str(t.getDb()))

		years = mdates.MonthLocator()
		months = mdates.DayLocator()
		yearsFmt = mdates.DateFormatter('%d-%m-%Y')

		fig, ax = plt.subplots()

		for key_tipo, value_tipo in data_plot.items():
			for key_vencimento, value_vencimento in value_tipo.items():
				ax.plot(value_vencimento[1], value_vencimento[0], label=str(key_tipo) + " (" + str(key_vencimento).replace(" 00:00:00", "") + ")")
				s = pd.Series(value_vencimento[0])
				ax.plot(value_vencimento[1], s.rolling(self._MM_WINDOW_SHORT).mean().tolist(), label=str(key_tipo) + " (" + str(key_vencimento).replace(" 00:00:00", "MM") + ")")
				ax.plot(value_vencimento[1], s.rolling(self._MM_WINDOW_LONG).mean().tolist(), label=str(key_tipo) + " (" + str(key_vencimento).replace(" 00:00:00", "MM") + ")")

			# format the ticks
			ax.xaxis.set_major_locator(years)
			ax.xaxis.set_major_formatter(yearsFmt)
			ax.xaxis.set_minor_locator(months)

			ax.set_facecolor('xkcd:black')

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
	estatisticas.plot(TipoTitulo.IPCA.value, 'compra', datetime.strptime('01/01/2047', '%d/%m/%Y'))