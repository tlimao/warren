import urllib.request
import ssl
from datetime import datetime
from common import *
from stnparser import StnPageParser, StnFileParser

class StnPageCrawler():

	def __init__(self):
		self.stnpageparser = StnPageParser()

		self.ctx = ssl.create_default_context()
		self.ctx.check_hostname = False
		self.ctx.verify_mode = ssl.CERT_NONE

	def crawling(self):
		if not OFFLINE_FLAG:
			try:
				stnPage = urllib.request.urlopen(STN_PAGE)
			
				return self.stnpageparser.parse(str(stnPage.read()))

			except:
				print("Offline Page File")
				stnPage = open(STN_OFFLINE_PAGE, "r", encoding='latin1')

				return self.stnpageparser.parse(stnPage.read().replace('\n',''))
		else:
			print("Offline Page File")
			stnPage = open(STN_OFFLINE_PAGE, "r", encoding='latin1')

			return self.stnpageparser.parse(stnPage.read().replace('\n',''))

class StnFileCrawler():

	def __init__(self):
		self.stnfileparser = StnFileParser()

		if not OFFLINE_FLAG:
			self.ctx = ssl.create_default_context()
			self.ctx.check_hostname = False
			self.ctx.verify_mode = ssl.CERT_NONE

			with urllib.request.urlopen(STN_URL, context=self.ctx) as u, \
			        open(STN_FILE, 'wb') as f:
			    f.write(u.read())

	def crawling(self):
		self.filedata = open(STN_FILE, "r")

		return self.stnfileparser.parse(self.filedata)

if __name__ == "__main__":
	page = StnFileCrawler()
	titulos_compra, data = page.crawling()

	for t in titulos_compra:
		print(t)