from datetime import datetime
from common import IR_ALIQUOTAS, IOF_ALIQUOTAS, NOVA_LIQUIDACAO
from titulo import Titulo, TipoTitulo
from stnpool import StnPool
import time

class Operation():

	def __init__(self, titulo, compraVenda, valorAplicado):
		self._titulo = titulo
		self._data_operacao = titulo.getDb()
		self._tipo_operacao = compraVenda
		self._pu_contratado = titulo.getPu('compra')
		self._dt_liquidacao = 2 if self._data_operacao < NOVA_LIQUIDACAO else 1
		self._valor_aplicado = valorAplicado
		self._qnt = valorAplicado / self._pu_contratado

	def calculaRendimentoTotal(self, pu_atual, data_atual):
		diff = pu_atual * self._qnt - self._valor_aplicado
		
		if diff > 0:
			ir = diff * self._ir(data_atual)
			iof = (diff - ir) * self._iof(data_atual)
			b3 = pu_atual * self._qnt * self._b3(data_atual)

			#print("IR: ", round(ir, 2), "IOF: ", round(iof, 2), "B3: ", round(b3, 2))

			return (diff - ir - iof - b3) / self._valor_aplicado
			#return (diff) / self._valor_aplicado

		else:
			return diff / self._valor_aplicado

	def calculaRendimentoAnual(self, pu_atual, data_atual):
		total_anos = ((data_atual - self._data_operacao).days - self._dt_liquidacao) / 365

		return self.calculaRendimentoTotal(pu_atual) / total_anos

	def calculaRendimento12Meses(self, pu_atual):
		pass

	def calculaRendimentoMensal(self, pu_atual, data_atual):
		total_meses = ((data_atual - self._data_operacao).days - self._dt_liquidacao) / 30

		return self.calculaRendimentoTotal(pu_atual, data_atual) / total_meses

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

	def resgatar(self, pu_atual, data_atual):
		return self._valor_aplicado * (1 + self.calculaRendimentoTotal(pu_atual, data_atual))

if __name__ == "__main__":
	titulos = [{
		'tt'  : 'IPCA+', 
		'dv'  : '15/05/2035',
		'db'  : '07/11/2016',
		'tc'  : '5,72',
		'puc' : '1054,78'
	}, {
		'tt'  : 'IPCA+', 
		'dv'  : '15/05/2035',
		'db'  : '01/12/2016',
		'tc'  : '6,18',
		'puc' : '979,62'
	}, {
		'tt'  : 'IPCA+', 
		'dv'  : '15/05/2035',
		'db'  : '10/01/2017',
		'tc'  : '5,7',
		'puc' : '1074,20'
	}, {
		'tt'  : 'IPCA+', 
		'dv'  : '15/05/2035',
		'db'  : '23/01/2017',
		'tc'  : '5,56',
		'puc' : '1104,54'
	}, {
		'tt'  : 'IPCA+', 
		'dv'  : '15/05/2035',
		'db'  : '02/02/2017',
		'tc'  : '5,47',
		'puc' : '1125,53'
	}]

	valores_aplicados = [305.88, 303.68, 322.26, 828.40, 438.95]
	precos_atuais = [1347.65, 1347.65, 1347.65, 1347.65, 1347.65]

	array_titulos = []

	for t in titulos:
		titulo = Titulo(t)
		print(titulo)
		array_titulos.append(titulo)


	for i in range(len(array_titulos)):
		operation = Operation(array_titulos[i],'compra', valores_aplicados[i])
		print(round(operation.calculaRendimentoTotal(precos_atuais[i], datetime.now()) * 100, 2))
