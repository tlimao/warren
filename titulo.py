class Titulo():

	self.TIPO_TITULO = 'tt'
	self.DATA_VENCIMENTO = 'dv'
	self.DATA_BASE = 
	self.TAXA_COMPRA_MANHA = 'tc'
	self.TAXA_VENDA_MANHA = 'tv'
	self.PU_COMPRA_MANHA = 'puc'
	self.PU_VENDA_MANHA = 'puv'
	self.PU_BASE_MANHA = 'pub'

	self.verbose = {
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
		
		for key, value in self.verbose:
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