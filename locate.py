#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RUN: python locate.py [goal] -- locate, clean or help

import urllib2
import urllib
import json
import copy
import sys

filename = "data_small"
my_mail = 'milkbread@freenet.de'
osm_url = 'http://nominatim.openstreetmap.org/search?'

def main(argv=None):
	if argv is None:
		argv = sys.argv
	try:
		goal = argv[1].replace('-','')
	except:
		raise ValueError("No goal defined!")

	if goal == 'locate':
		json_data = open(filename + ".json", "r")
		data = json.load(json_data)
		new_places = []

		for place in data["birth_places"]:
			print place.encode("latin_1")#.encode("utf-8")
			request =  urllib.urlencode({'q': place.encode("latin_1"), 'format': 'json', 'limit': '1', 'email':my_mail})
			# urllib2.urlopen(url)
			# Results in a json containing (only important): place_id_licence_bbox_lon_lat_display_name
			response = urllib2.urlopen(osm_url + request)
			resp_data = response.read().decode('utf-8')
			j_data = {}
			try:
				j_data = json.loads(resp_data)[0]
				new_place = {"name": place, 'coordinates': [j_data['lon'], j_data['lat']]}
			except:
				new_place = {"name": place, 'coordinates': "undefined"}
			try:
				d_names = j_data['display_name'].split(', ')
				new_place['county'] = d_names[len(d_names)-3]
			except:
				new_place['county'] = 'undefined'

			new_places.append(new_place)

		data['birth_places'] = new_places
		json_data.close()

		# save geoJSON to file
		with open(filename + "_located"+".json", "w") as file:
			file.write(json.dumps(data, indent=4))
		file.close()
	elif goal == 'clean':
		print 'going to clean'
	elif goal == 'help' or goal == 'h':
		print "Possible goals: locate, clean & help"
	else:
		raise ValueError("'%s' is no valid goal" % goal)

if __name__ == "__main__":
    sys.exit(main())
