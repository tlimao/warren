from html.parser import HTMLParser
from datetime import datetime
import re

class StnParser(HTMLParser):

	meta = { '0' : 'tt', '1' : 'dv', '2' : 'tc', '3' : 'vm', '4' : 'pu', '5' : 'cv', '6' : 'db' }
	state = [False, -1, 0]
	titulo = None
	titulos = []
	datetime_pattern = re.compile("(?P<dia>\d{2})\/(?P<mes>\d{2})\/(?P<ano>\d{4}) (?P<hora>\d{2}):(?P<min>\d{2})")

	def handle_starttag(self, startTag, attrs):
		if startTag == 'td':
			for name, value in attrs:
				if name == 'class' and 'listing0' in value:
					self.titulo = { 'cv' : self.state[2] }
					self.state[0] = True
					self.state[1] += 1

				elif name == 'class' and 'listing' in value:
					self.state[0] = True
					self.state[1] += 1

		else:
			self.state[0] = False
			self.state[1] = -1

	def handle_data(self, data):
		hora_atualizacao = re.findall(self.datetime_pattern, data)

		if hora_atualizacao != []:
			self.titulos.append(data)

		if data == " Investir ":
			self.state[2] = 0

		elif data == " Resgatar ":
			self.state[2] = 1

		if self.state[0] and data != ' ':
			if self.state[1] == 3 and self.state[2] == 0:
				pass

			elif self.state[1] == 3 and self.state[2] == 1:
				self.titulo[self.meta[str(self.state[1] + 1)]] = data

			else:
				self.titulo[self.meta[str(self.state[1])]] = data

		if self.state[0]:
			if (self.state[1] == 4 and self.state[2] == 0) or \
			   (self.state[1] == 3 and self.state[2] == 1):
				self.titulo['db'] = datetime.now().strftime("%Y/%m/%d")
				self.titulos.append(self.titulo)
				self.state[0] = False
				self.state[1] = -1

	def feed(self, data):
		super(StnParser, self).feed(data)

		return self.titulos