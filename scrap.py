from lxml import html
import requests
import json
import copy

COLLECTION = {
    "type": "AbgeordnetenCollection",
    "abgeordnete": [],
    "properties": {}
}

ABGEORDNETER = {
	"name": "",
	"party": -1,
	"born_date": "",
	"born_place": "",
	"profession": "",
	"url": "",
	"voted_by": "",
	"ward": "",
	"type": "Abgeordneter"
}

partys = []

page = requests.get('http://bundestag.de/bundestag/abgeordnete18/alphabet/index.html')
tree = html.fromstring(page.text)

# for link in tree.xpath('//div[@class="linkIntern"]//a//@href'):
# 	url = 'http://bundestag.de/bundestag/abgeordnete18' + link.replace('..','')
# 	print url
	# page2 = requests.get('http://bundestag.de/bundestag/abgeordnete18/')



link = tree.xpath('//div[@class="linkIntern"]//a//@href')[1]
url = 'http://bundestag.de/bundestag/abgeordnete18' + link.replace('..','')
abgeordneter = copy.deepcopy(ABGEORDNETER)
abgeordneter['url'] = url
page2 = requests.get(url)
tree2 = html.fromstring(page2.text)
heading = tree2.xpath('//div[@class="inhalt"]//h1/text()')[0].split(', ')
abgeordneter['name'] = heading[0]
abgeordneter['party'] = heading[1]
abgeordneter['profession'] = tree2.xpath('//div[@class="inhalt"]//p//strong/text()')[0].split(', ')
born = tree2.xpath('//div[@class="inhalt"]//p/text()')[1].replace('Geboren am ', '').split(' in ')
abgeordneter['born_date'] = born[0]
abgeordneter['born_place'] = born[1].split(';')[0]
abgeordneter['voted_by'] = tree2.xpath('//div[@id="context"]//div[@class="contextBox"]//h2/text()')[4]
abgeordneter['ward'] = tree2.xpath('//div[@id="context"]//div[@class="contextBox"]//div[@class="standardBox"]//strong/text()')[1]
print abgeordneter