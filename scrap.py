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
	"name_first": "",
	"name_last": "",
	"party": -1,
	"born_date": "",
	"born_place": "",
	"profession": "",
	"url": "",
	"voted_by": "",
	"ward": "",
	"type": "Abgeordneter"
}

def writeToJSON(data):
	# save geoJSON to file
	with open("data.json", "w") as file:
		file.write(json.dumps(data, indent=4))
	file.close()


partys = []

page = requests.get('http://bundestag.de/bundestag/abgeordnete18/alphabet/index.html')
tree = html.fromstring(page.text)
collection = copy.deepcopy(COLLECTION)

for node in tree.xpath('//div[@class="linkIntern"]//a')[:10]:
	link = node.values()[0]
	name = node.text.replace("\n","").split(", ")
	last_name = name[0]
	first_name = name[1]
	abgeordneter = copy.deepcopy(ABGEORDNETER)
	abgeordneter['name_first'] = name[0]
	abgeordneter['name_last'] = name[1]
	url = 'http://bundestag.de/bundestag/abgeordnete18' + link.replace('..','')
	abgeordneter['url'] = url
	print "Reading 'Abgeordneter' from: ", abgeordneter['url']
	page2 = requests.get(url)
	tree2 = html.fromstring(page2.text)
	abgeordneter['party'] = tree2.xpath('//div[@class="inhalt"]//h1/text()')[0].split(', ')[1]
	abgeordneter['profession'] = tree2.xpath('//div[@class="inhalt"]//p//strong/text()')[0].split(', ')
	born = tree2.xpath('//div[@class="inhalt"]//p/text()')[1].replace('Geboren am ', '').split(' in ')
	abgeordneter['born_date'] = born[0]
	try:
		abgeordneter['born_place'] = born[1].split(';')[0]
	except:
		abgeordneter['born_place'] = "Not defined"
	try:
		abgeordneter['voted_by'] = tree2.xpath('//div[@id="context"]//div[@class="contextBox"]//h2/text()')[4]
		abgeordneter['ward'] = tree2.xpath('//div[@id="context"]//div[@class="contextBox"]//div[@class="standardBox"]//strong/text()')[1]
	except:
		print abgeordneter['name'], "makes problems!"
	collection["abgeordnete"].append(abgeordneter)

writeToJSON(collection)