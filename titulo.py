class Titulo():

	TIPO_TITULO = 'tt'
	DATA_VENCIMENTO = 'dv'
	DATA_BASE = 'db'
	TAXA_COMPRA_MANHA = 'tc'
	TAXA_VENDA_MANHA = 'tv'
	PU_COMPRA_MANHA = 'puc'
	PU_VENDA_MANHA = 'puv'
	PU_BASE_MANHA = 'pub'

	verbose = {
		'tt' : 'Tipo Titulo', 
		'dv' : 'Data Vencimento',
		'db' : 'Data Base',
		'tc' : 'Taxa Compra Manha',
		'tv' : 'Taxa Venda Manha',
		'puc' : 'PU Compra Manha',
		'puv' : 'PU Venda Manha',
		'pub' : 'PU Base Manha'
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
		return self._info_titulo['dv']

	def getDb(self):
		return self._info_titulo['db']

	def getTc(self):
		return self._info_titulo['tc']

	def getTv(self):
		return self._info_titulo['tv']

	def getPuc(self):
		return self._info_titulo['puc']

	def getPuv(self):
		return self._info_titulo['puv']

	def getPub(self):
		return self._info_titulo['pub']

	def getInfo(self, value):
		return self._info_titulo[value]

	def __str__(self):
		strTitulo = ""
		for key, value in self._info_titulo.items():
			strTitulo += "{0}: {1}\n".format(self.verbose[key], value)

		return strTitulo[:-1]