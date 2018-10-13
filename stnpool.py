import threading
import time
from stncrawler import StnPageCrawler, StnFileCrawler
from datetime import datetime
from titulo import TipoTitulo, Titulo

class StnPool(threading.Thread):

	def __init__(self):
		self._isFirsTime = True
		self._lastUpdate = None

		self._titulos_ativos = None

		self._poolTitulos = None
		self._titulosCompra = None
		self._titulosVenda = None
		
		self._poolHistoricoTitulos = None
		self._historicoTitulosCompra = None
		self._historicoTitulosVenda = None

		self._stnpagecrawler = StnPageCrawler()
		self._stnfilecrawler = StnFileCrawler()

		super(StnPool, self).__init__()

	def getTitulos(self):
		return self._poolTitulos

	def getTitulosCompra(self, tipo):
		return self._getTitulo(tipo, compraVenda='compra')

	def getTitulosVenda(self, tipo):
		return self._getTitulo(tipo, compraVenda='venda')

	def _getTitulo(self, tipo, compraVenda=None):
		query_result = []
		
		if compraVenda != None:
			for t in self._poolTitulos:
				if tipo.name in t.getTt().upper():
					if compraVenda == 'compra' and t.isCompra():
						query_result.append(t)
					elif compraVenda == 'venda' and t.isVenda():
						query_result.append(t)
		else:
			query_result = self._poolTitulos

		return query_result

	def getHistoricoTitulos(self):
		return self._poolHistoricoTitulos

	def getHistoricoTitulosCompra(self, tipo):
		return self._getHistoricoTitulo(tipo, compraVenda='compra')

	def getHistoricoTitulosVenda(self, tipo):
		return self._getHistoricoTitulo(tipo, compraVenda='venda')

	def _getHistoricoTitulo(self, tipo, compraVenda=None):
		query_result = []
		
		if compraVenda != None:
			for t in self._poolHistoricoTitulos:
				if tipo.name in t.getTt().upper():
					if compraVenda == 'compra' and t.isCompra():
						query_result.append(t)
					elif compraVenda == 'venda' and t.isVenda():
						query_result.append(t)
		else:
			query_result = self._poolHistoricoTitulos

		return query_result

	def getTitulosAtivosCompra(self):
		return self._titulos_ativos['compra']

	def getTitulosAtivosVenda(self):
		return self._titulos_ativos['venda']

	def getTitulosAtivos(self):
		return self._titulos_ativos

	def run(self):
		#while True:
		# Crawling na página do Tesouro para pegar os valores de venda atuais
		self._titulosCompra, self._titulosVenda, stn_page_datetime = self._stnpagecrawler.crawling()

		if self._isFirsTime or stn_page_datetime != self._lastUpdate:
			self._isFirsTime = False
			self._lastUpdate = stn_page_datetime
			self._poolTitulos = self._titulosVenda + self._titulosCompra
			self._poolTitulos.sort(key=lambda x: x.getDb())

			# Dict para guardar os tipos de título ativos no site do tesouro
			self._titulos_ativos = { 'compra' : {}, 'venda' : {} }

			for t in self._titulosCompra:
				titulo_tipo = t.getTt().upper()
				titulo_vencimento = t.getDv()

				self._titulos_ativos['compra'][titulo_tipo] = 'ativo'

			for t in self._titulosVenda:
				titulo_tipo = t.getTt().upper()
				titulo_vencimento = t.getDv()
				
				self._titulos_ativos['venda'][titulo_tipo] = 'ativo'

		# Atualiza os dados históricos
		if self._lastUpdate == None or datetime.now().day != self._lastUpdate.day:
			self._historicoTitulosCompra, self._historicoTitulosVenda, stn_file_datetime = self._stnfilecrawler.crawling()
			self._poolHistoricoTitulos = self._historicoTitulosVenda + self._historicoTitulosCompra
			self._poolHistoricoTitulos.sort(key=lambda x: x.getDb())

