from datetime import datetime
from common import IR_ALIQUOTAS, IOF_ALIQUOTAS, NOVA_LIQUIDACAO
from titulo import Titulo, TipoTitulo
from stnpool import StnPool
import time

class Operation():

	def __init__(self, titulo, compraVenda, qnt):
		self._titulo = titulo
		self._data_operacao = titulo.getDb()
		self._tipo_operacao = compraVenda
		self._pu_contratado = titulo.getPu('compra')
		self._dt_liquidacao = 2 if self._data_operacao < NOVA_LIQUIDACAO else 1
		self._qnt = qnt

	def calculaRendimentoTotal(self, pu_atual, data_atual):
		diff = pu_atual - self._pu_contratado
		
		if diff > 0:
			ir = diff * self._ir(data_atual)
			iof = (diff - ir) * self._iof(data_atual)
			b3 = pu_atual * self._b3(data_atual)

			print("IR: ", round(ir * self._qnt, 2), "IOF: ", round(iof * self._qnt, 2), "B3: ", round(b3 * self._qnt, 2))

			return (diff - ir - iof - b3) / self._pu_contratado

		else:
			return diff / self._pu_contratado

	def calculaRendimentoAnual(self, pu_atual, data_atual):
		total_anos = ((data_atual - self._data_operacao).days - self._dt_liquidacao) / 365

		return self.calculaRendimentoTotal(pu_atual) / total_anos

	def calculaRendimento12Meses(self, pu_atual):
		pass

	def calculaRendimentoMensal(self, pu_atual, data_atual):
		total_meses = ((data_atual - self._data_operacao).days - self._dt_liquidacao) / 30

		return self.calculaRendimentoTotal(pu_atual) / total_meses

	def getTipo(self):
		pass

	def getDate(self):
		return self._data_operacao

	def getTitulo(self):
		return self._titulo

	def _iof(self, data):
		diff = (data - self._data_operacao).days - self._dt_liquidacao
		
		if diff > 30:
			return 0

		else:
			return IOF_ALIQUOTAS[str(diff)]

	def _ir(self, data):
		diff = (data - self._data_operacao).days - self._dt_liquidacao

		if diff <= 180:
			return IR_ALIQUOTAS['180']

		elif diff > 180 and diff <= 360:
			return IR_ALIQUOTAS['181-360']

		elif diff > 360 and diff <= 720:
			return IR_ALIQUOTAS['361-720']

		else:
			return IR_ALIQUOTAS['720']

	def _b3(self, data):
		if data.month < 7:
			diff = data - datetime.strptime("01/01/{0}".format(data.year), '%d/%m/%Y')
			diff_base =  datetime.strptime("01/07/{0}".format(data.year), '%d/%m/%Y') - datetime.strptime("01/01/{0}".format(data.year), '%d/%m/%Y')

			taxa = 0.0015 * diff / diff_base
		else: 
			diff = data - datetime.strptime("01/07/{0}".format(data.year), '%d/%m/%Y')
			diff_base =  datetime.strptime("01/01/{0}".format(data.year + 1), '%d/%m/%Y') - datetime.strptime("01/07/{0}".format(data.year), '%d/%m/%Y')

			taxa = 0.0015 * diff / diff_base

		return taxa

	def resgatar(self, pu, data_atual):
		return self._qnt * (1 + self.calculaRendimentoTotal(pu, data_atual))
		