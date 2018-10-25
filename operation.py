from datetime import datetime
from common import IR_ALIQUOTAS, IOF_ALIQUOTAS, NOVA_LIQUIDACAO
from titulo import Titulo, TipoTitulo
from stnpool import StnPool
import time

class Operation():

	def __init__(self, titulo, qnt):
		self._titulo = titulo
		self._data_operacao = titulo.getDb()
		self._tipo_operacao = 'compra' if titulo.isCompra() else 'venda'
		self._pu_contratado = titulo.getPu()
		self._dt_liquidacao = 2 if self._data_operacao < NOVA_LIQUIDACAO else 1
		self._qnt = qnt

	def calculaRendimentoTotal(self, pu_atual):
		diff = pu_atual - self._pu_contratado
		
		if diff > 0:
			ir = diff * self._ir()
			iof = (diff - ir) * self._iof()
			b3 = pu_atual * self._b3()

			print("IR: ", round(ir * self._qnt, 2))
			print("IOF: ", round(iof * self._qnt, 2))
			print("B3: ", round(b3 * self._qnt, 2))

			return (diff - ir - iof - b3) / self._pu_contratado

		else:
			return diff / self._pu_contratado

	def calculaRendimentoAnual(self, pu_atual):
		total_anos = ((datetime.now() - self._data_operacao).days - self._dt_liquidacao) / 365

		return self.calculaRendimentoTotal(pu_atual) / total_anos

	def calculaRendimento12Meses(self, pu_atual):
		pass

	def calculaRendimentoMensal(self, pu_atual):
		total_meses = ((datetime.now() - self._data_operacao).days - self._dt_liquidacao) / 30

		return self.calculaRendimentoTotal(pu_atual) / total_meses

	def getTipo(self):
		pass

	def getDate(self):
		return self._data_operacao

	def getTitulo(self):
		return self._titulo

	def _iof(self):
		diff = (datetime.now() - self._data_operacao).days - self._dt_liquidacao
		
		if diff > 30:
			return 0

		else:
			return IOF_ALIQUOTAS[diff]

	def _ir(self):
		diff = (datetime.now() - self._data_operacao).days - self._dt_liquidacao

		if diff <= 180:
			return IR_ALIQUOTAS['180']

		elif diff > 180 and diff <= 360:
			return IR_ALIQUOTAS['181-360']

		elif diff > 360 and diff <= 720:
			return IR_ALIQUOTAS['361-720']

		else:
			return IR_ALIQUOTAS['720']

	def _b3(self):
		date = datetime.now()
		
		if date.month < 7:
			diff = date - datetime.strptime("01/01/{0}".format(date.year), '%d/%m/%Y')
			diff_base =  datetime.strptime("01/07/{0}".format(date.year), '%d/%m/%Y') - datetime.strptime("01/01/{0}".format(date.year), '%d/%m/%Y')

			taxa = 0.0015 * diff / diff_base
		else: 
			diff = date - datetime.strptime("01/07/{0}".format(date.year), '%d/%m/%Y')
			diff_base =  datetime.strptime("01/01/{0}".format(date.year + 1), '%d/%m/%Y') - datetime.strptime("01/07/{0}".format(date.year), '%d/%m/%Y')

			taxa = 0.0015 * diff / diff_base

		return taxa

if __name__ == "__main__":
	titulo_info = [
		[{
			'tt' : 'Tesouro Prefixado',
			'dv' : '01/01/2023',
			'db' : '23/05/2017',
			'tc' : '11,67',
			'pu' : '539,71'
		}, 4.81],
		[{
			'tt' : 'Tesouro Prefixado',
			'dv' : '01/01/2023',
			'db' : '05/09/2017',
			'tc' : '9,68',
			'pu' : '613,16'
		}, 0.82],
		[{
			'tt' : 'Tesouro Prefixado',
			'dv' : '01/01/2023',
			'db' : '12/09/2017',
			'tc' : '9,61',
			'pu' : '616,14'
		}, 6.04],
		[{
			'tt' : 'Tesouro Prefixado',
			'dv' : '01/01/2023',
			'db' : '08/11/2017',
			'tc' : '9,96',
			'pu' : '614,82'
		}, 0.12],
	]

	stn_pool = StnPool()
	stn_pool.start()
	time.sleep(20)

	titulos_venda = stn_pool.getTitulosVenda(TipoTitulo.PRE)

	for tf in titulo_info:
		titulo = Titulo(tf[0])

		titulo_atual = None

		for t in titulos_venda:
			if t.getTt() == str(titulo.getTt() + " " + str(titulo.getDv().year))  and t.getDv() == titulo.getDv():
				titulo_atual = t
				break

		operacao = Operation(titulo, tf[1])

		print("Rendimento Total: ", round(operacao.calculaRendimentoTotal(titulo_atual.getPu())*100, 2), "%")
		