import threading
import time
from stncrawler import StnCrawler
from datetime import datetime
from titulo import TipoTitulo

class StnPool(threading.Thread):

	def __init__(self):
		self._isFirsTime = True
		self._lastUpdate = None
		self._poolTitulos = None
		self._crawler = StnCrawler()
		self._titulosCompra = None
		self._titulosVenda = None

		super(StnPool, self).__init__()

	def getTitulos(self):
		return self._poolTitulos

	def getTitulosCompra(self, tipo):
		query_result = []
		
		for t in self._poolTitulos:
			if tipo.name in t['tt'] and t['cv'] == 0:
				query_result.append(t)

		return query_result

	def getTitulosVenda(self, tipo):
		query_result = []
		
		for t in self._poolTitulos:
			if tipo.name in t['tt'] and t['cv'] == 1:
				query_result.append(t)

		return query_result

	def getTitulo(self, tipo, compraVenda=None):
		query_result = []
		
		for t in self._poolTitulos:
			if tipo.name in t['tt']:
				if compraVenda == None:
					query_result.append(t)
				elif compraVenda == 'compra' and t['cv'] == 0:
					query_result.append(t)
				elif compraVenda == 'venda' and t['cv'] == 1:
					query_result.append(t)

		return query_result

	def run(self):
		dados_titulos = self._crawler.crawling()

		data_hora_stn = datetime.strptime(dados_titulos[-1], '%d/%m/%Y %H:%M')

		if self._isFirsTime:
			self._isFirsTime = False
			self._lastUpdate = data_hora_stn
			# Popular Pool
			self._poolTitulos = dados_titulos[:-1]

		else:
			if data_hora_stn != self._lastUpdate:
				# Atualizar Pool
				self._poolTitulos = dados_titulos[:-1]

		for titulo in self._poolTitulos:
			self._titulosCompra = []
			self._titulosVenda = []
			# Títulos para compra
			
			if titulo['cv'] == 0:
				self._titulosCompra.append(titulo)
			# Titulos para venda
			else:
				self._titulosVenda.append(titulo)
