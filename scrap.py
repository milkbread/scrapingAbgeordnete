from lxml import html
import requests

page = requests.get('http://bundestag.de/bundestag/abgeordnete18/alphabet/index.html')
tree = html.fromstring(page.text)

# for link in tree.xpath('//div[@class="linkIntern"]//a//@href'):
# 	url = 'http://bundestag.de/bundestag/abgeordnete18' + link.replace('..','')
# 	print url
	# page2 = requests.get('http://bundestag.de/bundestag/abgeordnete18/')



link = tree.xpath('//div[@class="linkIntern"]//a//@href')[0]
url = 'http://bundestag.de/bundestag/abgeordnete18' + link.replace('..','')
print url