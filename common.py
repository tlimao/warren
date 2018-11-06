from datetime import datetime

STN_FILE = "data/PrecoTaxaTesouroDireto.csv"
STN_URL = "https://www.tesourotransparente.gov.br/ckan/dataset/df56aa42-484a-4a59-8184-7676580c81e3/resource/796d2059-14e9-44e3-80c9-2d9e30b405c1/download/PrecoTaxaTesouroDireto.csv"
STN_PAGE_FILE = "data/PrecosTaxaTesouroDireto.html"
STN_PAGE = "http://www.tesouro.fazenda.gov.br/tesouro-direto-precos-e-taxas-dos-titulos"
STN_OFFLINE_PAGE = "data/PrecoTaxaTesouroDireto.html" 

IR_ALIQUOTAS = {
	'720' : 0.15, 
	'361-720' : 0.175, 
	'181-360' : 0.20, 
	'180' : 0.225
}

IOF_ALIQUOTAS = {
	'1'  : 0.96, '11' : 0.63, '21' : 0.30,
	'2'  : 0.93, '12' : 0.60, '22' : 0.26,
	'3'  : 0.90, '13' : 0.56, '23' : 0.23,
	'4'  : 0.86, '14' : 0.53, '24' : 0.20,
	'5'  : 0.83, '15' : 0.50, '25' : 0.16,
	'6'  : 0.80, '16' : 0.46, '26' : 0.13,
	'7'  : 0.76, '17' : 0.43, '27' : 0.10,
	'8'  : 0.73, '18' : 0.40, '28' : 0.06,
	'9'  : 0.70, '19' : 0.36, '29' : 0.03,
	'10' : 0.66, '20' : 0.33, '30' : 0.00
}

NOVA_LIQUIDACAO = datetime.strptime("05/02/2018", '%d/%m/%Y')

OFFLINE_FLAG = True