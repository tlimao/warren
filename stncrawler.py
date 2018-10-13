import urllib.request
import ssl
from datetime import datetime
from common import *
from stnparser import StnPageParser, StnFileParser

class StnPageCrawler():

	def __init__(self):
		self.ctx = ssl.create_default_context()
		self.ctx.check_hostname = False
		self.ctx.verify_mode = ssl.CERT_NONE

		self.stnpageparser = StnPageParser()

	def crawling(self):
		stnPage = urllib.request.urlopen(STN_PAGE)
		
		return self.stnpageparser.parse(str(stnPage.read()))

class StnFileCrawler():

	def __init__(self):
		#self.ctx = ssl.create_default_context()
		#self.ctx.check_hostname = False
		#self.ctx.verify_mode = ssl.CERT_NONE

		self.stnfileparser = StnFileParser()

		#with urllib.request.urlopen(STN_URL, context=self.ctx) as u, \
		#        open(STN_FILE, 'wb') as f:
		#    f.write(u.read())

	def crawling(self):
		self.filedata = open(STN_FILE, "r")

		return self.stnfileparser.parse(self.filedata)