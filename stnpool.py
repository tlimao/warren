import threading
import time
from stncrawler import StnPageCrawler, StnFileCrawler
from datetime import datetime
from titulo import TipoTitulo, Titulo

class StnPool():#threading.Thread):

	def __init__(self):
		self._isFirsTime = True
		self._lastUpdate = None

		self._titulos_ativos = None

		self._poolTitulos = None
		self._titulosCompra = None
		self._titulosVenda = None
		
		self._historicoTitulos = None

		self._stnpagecrawler = StnPageCrawler()
		self._stnfilecrawler = StnFileCrawler()
		self.process()
		#super(StnPool, self).__init__()

	def getTitulo(self, tipo, vencimento, date=None):
		query_result = []

		for t in self._historicoTitulos:
			if t.getDv() == vencimento and t.getTt() == tipo:
				if date != None:
					if date == t.getDb():
						query_result.append(t)
				else:
					query_result.append(t)
		
		return query_result

	def getTitulos(self):
		return self._poolTitulos

	def getHistoricoTitulos(self):
		return self._historicoTitulos

	def getTitulosAtivos(self):
		return self._titulos_ativos

	def process(self):
		#while True:
		# Crawling na página do Tesouro para pegar os valores de venda atuais
		self._titulosCompra, self._titulosVenda, stn_page_datetime = self._stnpagecrawler.crawling()

		if self._isFirsTime or stn_page_datetime != self._lastUpdate:
			self._isFirsTime = False
			#self._lastUpdate = stn_page_datetime
			self._poolTitulos = self._titulosVenda + self._titulosCompra
			self._poolTitulos.sort(key=lambda x: x.getDb())

			# Dict para guardar os tipos de título ativos no site do tesouro
			self._titulos_ativos = { 'compra' : {}, 'venda' : {} }

			for t in self._titulosCompra:
				titulo_tipo = t.getTt()
				titulo_vencimento = t.getDv()
				if titulo_tipo in self._titulos_ativos['compra']:
					self._titulos_ativos['compra'][titulo_tipo].append(titulo_vencimento)
				else:
					self._titulos_ativos['compra'][titulo_tipo] = [titulo_vencimento]

			for t in self._titulosVenda:
				titulo_tipo = t.getTt()
				titulo_vencimento = t.getDv()
				
				if titulo_tipo in self._titulos_ativos['venda']:
					self._titulos_ativos['venda'][titulo_tipo].append(titulo_vencimento)
				else:
					self._titulos_ativos['venda'][titulo_tipo] = [titulo_vencimento]

		# Atualiza os dados históricos
		if self._lastUpdate == None or datetime.now().day != self._lastUpdate.day:
			self._historicoTitulos, stn_file_datetime = self._stnfilecrawler.crawling()
			self._historicoTitulos.sort(key=lambda x: x.getDb())

if __name__ == "__main__":
	stnpool= StnPool()
	result = stnpool.getTitulo(TipoTitulo.PRE.value, datetime.strptime('01/01/2023', '%d/%m/%Y'), datetime.strptime('10/10/2018', '%d/%m/%Y'))
	for r in result:
		print(r)