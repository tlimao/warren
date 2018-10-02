import threading
import urllib.request
import ssl
from datetime import datetime, timedelta
from titulo import Titulo
from common import *
import pandas as pd

class StnDaemon(threading.Thread):

	_filedata = None
	_isUpdate = False
	_titulos = None
	_baseData = None

	def __init__(self):
		self._titulos = []
		self._baseData = datetime.now()
		super(StnDaemon, self).__init__()

	def run(self):
		self.refreshData()
		line = self._filedata.readline()

		while line != "":
			tituloInfo = self.parsing(line)
			novoTitulo = Titulo(tituloInfo)
			# Tratamento se deve ou não ser inserido no pool
			if novoTitulo.getDv() >= self._baseData: 
				self._titulos.append(novoTitulo)

			line = self._filedata.readline()

	def refreshData(self):
		if not self._isUpdate:
			# Colocar um curl para o STN
			ctx = ssl.create_default_context()
			ctx.check_hostname = False
			ctx.verify_mode = ssl.CERT_NONE

			with urllib.request.urlopen(STN_URL, context=ctx) as u, \
			        open(STN_FILE, 'wb') as f:
			    f.write(u.read())

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

	def getTitulos(self):
		return self._titulos