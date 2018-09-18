import threading
from titulo import Titulo
from common import *

class StnDaemon(threading.Thread):

	_filedata = None
	_isUpdate = False

	def run(self):
		self.refreshData()
		line = self._filedata.readline()

		while line != "":
			tituloInfo = self.parsing(line)
			novoTitulo = Titulo(tituloInfo)
			print(novoTitulo)
			
			line = self._filedata.readline()

	def refreshData(self):
		if not self._isUpdate:
			# Colocar um curl para o STN
			self._filedata = open(STN_FILE, "r")
			# Descarta 1ª Linha
			self._filedata.readline()
			self._isUpdate = True

	def parsing(self, rawData):
		values = rawData.replace('\n', '').split(';')
		tituloInfo = {}

		idx = 0

		for key, value in Titulo.verbose.items():
			tituloInfo[key] = values[idx]
			idx += 1

		return tituloInfo

if __name__ == "__main__":
	daemon = StnDaemon()
	daemon.start()