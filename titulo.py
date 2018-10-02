from datetime import datetime
from enum import Enum

class Titulo():

	TIPO_TITULO = 'tt'
	DATA_VENCIMENTO = 'dv'
	DATA_BASE = 'db'
	TAXA_COMPRA = 'tc'
	TAXA_VENDA = 'tv'
	PU_COMPRA= 'puc'
	PU_VENDA = 'puv'

	verbose = {
		'tt' : 'Tipo Titulo', 
		'dv' : 'Data Vencimento',
		'db' : 'Data Base',
		'tc' : 'Taxa Compra',
		'tv' : 'Taxa Venda',
		'puc' : 'PU Compra',
		'puv' : 'PU Venda'
	}

	def __init__(self, data):

		self._info_titulo = {}
		
		for key, value in self.verbose.items():
			if data[key].replace(',', '').isdigit():
				self._info_titulo[key] = eval(data[key].replace(',', '.'))

			else:
				self._info_titulo[key] = data[key]

	def getInfoAll(self):
		return self._info_titulo

	def getTt(self):
		return self._info_titulo['tt']

	def getDv(self):
		return datetime.strptime(self._info_titulo['dv'], '%d/%m/%Y')

	def getDb(self):
		return datetime.strptime(self._info_titulo['db'], '%d/%m/%Y')

	def getTc(self):
		return self._info_titulo['tc']

	def getTv(self):
		return self._info_titulo['tv']

	def getPuc(self):
		return self._info_titulo['puc']

	def getPuv(self):
		return self._info_titulo['puv']

	def getInfo(self, value):
		return self._info_titulo[value]

	def __str__(self):
		strTitulo = ""
		for key, value in self._info_titulo.items():
			strTitulo += "{0}: {1}\n".format(self.verbose[key], value)

		return strTitulo[:-1]

class TipoTitulo(Enum):

	IPCA = "IPCA"
	SELIC = "SELIC"
	PRE = "PREFIXADO"