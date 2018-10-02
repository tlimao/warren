import urllib.request
import ssl
from datetime import datetime
from common import *
from stnparser import StnParser

class StnCrawler():

	def __init__(self):
		self.ctx = ssl.create_default_context()
		self.ctx.check_hostname = False
		self.ctx.verify_mode = ssl.CERT_NONE

		self.stnparser = StnParser()

	def crawling(self):
		stnPage = urllib.request.urlopen(STN_PAGE)

		return self.stnparser.feed(str(stnPage.read()))