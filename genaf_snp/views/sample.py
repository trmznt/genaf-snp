
from genaf_snp.views import *

class SNPSampleExtensionViewer(object):

	def __init__(self, request, sample):
		self.request = request
		self.sample = sample


	def extend(self, html):

		# we extend the html
		html.add( div('SNP list') )