#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import html
import requests
import json
import copy

COLLECTION = {
    "type": "AbgeordnetenCollection",
    "abgeordnete": [],
    "parties": [],
    "votings": [],
    "professions": [],
    "birth_places": [],
    "properties": {}
}

ABGEORDNETER = {
	"name_first": "",
	"name_last": "",
	"party": -1,
	"born_date": "",
	"born_place": "",
	"profession": [],
	"url": "",
	"voted_by": "",
	"ward": "",
	"type": "Abgeordneter"
}

ENCODING = "latin1"

def writeToJSON(data):
	# save geoJSON to file
	with open("data.json", "w") as file:
		file.write(json.dumps(data, indent=4))
	file.close()

page = requests.get('http://bundestag.de/bundestag/abgeordnete18/alphabet/index.html')
tree = html.fromstring(page.text)
collection = copy.deepcopy(COLLECTION)

for node in tree.xpath('//div[@class="linkIntern"]//a'):
	link = node.values()[0]
	name = node.text.replace("\n","").split(", ")
	abgeordneter = copy.deepcopy(ABGEORDNETER)
	abgeordneter['name_first'] = name[1]
	abgeordneter['name_last'] = name[0]
	url = 'http://bundestag.de/bundestag/abgeordnete18' + link.replace('..','')
	abgeordneter['url'] = url
	print "Reading 'Abgeordneter' from: ", abgeordneter['name_first'], abgeordneter['name_last']
	page2 = requests.get(url)
	tree2 = html.fromstring(page2.text)
	party = tree2.xpath('//div[@class="inhalt"]//h1/text()')[0].split(', ')[1]
	if not party in collection['parties']:
		collection['parties'].append(party)
	abgeordneter['party'] = collection['parties'].index(party)
	for profession in tree2.xpath('//div[@class="inhalt"]//p//strong/text()')[0].split(', '):
	# profession = tree2.xpath('//div[@class="inhalt"]//p//strong/text()')[0].split(', ')
		if not profession in collection['professions']:
			collection['professions'].append(profession)
		abgeordneter['profession'].append(collection['professions'].index(profession))
	born = tree2.xpath('//div[@class="inhalt"]//p/text()')[1].replace('Geboren am ', '').split(' in ')
	abgeordneter['born_date'] = born[0]
	try:
		birth = born[1].split(';')[0].split(',')[0]
		if not birth in collection['birth_places']:
			collection['birth_places'].append(birth)
		abgeordneter['born_place'] = collection['birth_places'].index(birth)
	except:
		abgeordneter['born_place'] = "Not defined"
	try:
		voting = tree2.xpath('//div[@id="context"]//div[@class="contextBox"]//h2/text()')[4]
		if not voting in collection['votings']:
			collection['votings'].append(voting)
		abgeordneter['voted_by'] = collection['votings'].index(voting)
		abgeordneter['ward'] = tree2.xpath('//div[@id="context"]//div[@class="contextBox"]//div[@class="standardBox"]//strong/text()')[1]
	except:
		print abgeordneter['name_last'], "makes problems!"
	collection["abgeordnete"].append(abgeordneter)

writeToJSON(collection)