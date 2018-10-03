import pandas as pd
import time
from titulo import TipoTitulo
from stndaemon import StnDaemon
from datetime import datetime

class StnEstatisticas():

	_array_titulos = {}

	_MmL = []
	_MmE = []

	_data_inicial = 0#Padrão é para ser now() - 1 ano
	_data_final = 0#Padrão é para ser now()

	def __init__(self):
		self._stndaemon = StnDaemon()
		self._stndaemon.start()

	def processData(self):
		self._initArrayTitulos()

		titulos = self._stndaemon.getTitulos()

		for titulo in titulos:
			tipo = titulo.getTt().upper()
			vencimento = titulo.getDv()

			if vencimento > datetime.now():
				if TipoTitulo.IPCA.value in tipo:
					self._array_titulos[TipoTitulo.IPCA.value].append(titulo)
				elif TipoTitulo.PRE.value in tipo:
					self._array_titulos[TipoTitulo.PRE.value].append(titulo)

		print(len(self._array_titulos[TipoTitulo.IPCA.value]))
		print(len(self._array_titulos[TipoTitulo.PRE.value]))

	def _initArrayTitulos(self):
		for tipo in list(TipoTitulo):
			self._array_titulos[tipo.value] = []

	def getMmL(self):
		pass

	def getMmE(self):
		pass

if __name__ == '__main__':
	estatisticas = StnEstatisticas()
	time.sleep(10)
	estatisticas.processData()
