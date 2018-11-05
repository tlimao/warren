from datetime import datetime
from enum import Enum

class Titulo():

	verbose_keys = {
		 'Tipo Titulo'           : 'tt', 
		 'Data Vencimento'       : 'dv',
		 'Data Base'             : 'db',
		 'Taxa Compra'           : 'tc',
		 'Taxa Venda'      	     : 'tv',
		 'Valor Mínimo'          : 'vm',
		 'Preço Unitário Compra' : 'puc',
		 'Preço Unitário Venda'  : 'puv'
	}

	keys_verbose = {
		'tt'  : 'Tipo Titulo', 
		'dv'  : 'Data Vencimento',
		'db'  : 'Data Base',
		'tc'  : 'Taxa Compra',
		'tv'  : 'Taxa Venda',
		'vm'  : 'Valor Mínimo',
		'puc' : 'Preço Unitário Compra',
		'puv' : 'Preço Unitário Venda'
	}

	def __init__(self, data):

		self._info_titulo = {}
		
		for key, value in data.items():
			if data[key].replace(',', '').replace('.', '').isdigit():
				self._info_titulo[key] = eval(data[key].replace('.', '').replace(',', '.'))

			else:
				self._info_titulo[key] = data[key]

	def getVm(self):
		fracao_titulo = self._info_titulo['puc'] / 100

		valor_minimo = 0

		while valor_minimo < 30:
			valor_minimo += fracao_titulo

		return valor_minimo

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

	def getPu(self, compraVenda=None):
		if compraVenda == None:
			return self._info_titulo['puc'], self._info_titulo['puv']
		else:
			return self._info_titulo['puc'] if compraVenda == 'compra' else self._info_titulo['puc']

	def getInfo(self, value):
		return self._info_titulo[value]

	def __str__(self):
		strTitulo = ""
		for key, value in self._info_titulo.items():
			strTitulo += "{0}: {1}\n".format(self.keys_verbose[key], value)

		return strTitulo[:-1]

class TipoTitulo(Enum):

	IPCA = "IPCA+"
	IPCA_JUROS_SEMESTRAIS = "IPCA+ com Juros Semestrais"
	SELIC = "Selic"
	PRE = "Prefixado"
	PRE_JUROS_SEMESTRAIS = "Prefixado com Juros Semestrais"
