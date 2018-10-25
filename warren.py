from stnpool import StnPool
from operation import Operation
from titulo import Titulo, TipoTitulo
import time
from datetime import datetime, timedelta
import pandas as pd

class Warren():

	def __init__(self):
		self._stnpool = StnPool()
		self._stnpool.start()
		print("carregando dados para simular ...")
		time.sleep(30)

		self._titulos_ativos = self._stnpool.getTitulosAtivos()
		self._array_titulos = {}

		self._data_plot = {}
		self._MmL = []
		self._MmE = []

		self._data_final = datetime.now()
		self._data_inicial = self._data_final + timedelta(days=-180)

		self._MM_WINDOW_SHORT = 2
		self._MM_WINDOW_LONG = 15
		print("processando dados ...")
		self._processData()

		self._saldo_disponivel = 1000.00

		self._minhas_operacoes = None

	def _processData(self):
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

	def simular(self):
		data_atual = self._data_inicio_simulacao

		while data_atual < self._data_fim_simulacao:



			data_atual += timedelta(days=1)

	def select(self, compraVenda, tipo, vencimento):
		print(self._data_plot[compraVenda][tipo][vencimento]['taxas'])
		print(self._data_plot[compraVenda][tipo][vencimento]['datas'])

if __name__ == "__main__":
	warren = Warren()
	warren.select(TipoTitulo.PRE.value, 'compra', datetime.strptime('01/01/2026', '%d/%m/%Y'))

