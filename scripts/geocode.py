#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import json
import requests
import csv, codecs
import sys
import time
import argparse

def uniencoder(foo):
	if isinstance(foo,basestring):
		boo = foo.encode('utf8')
	else:
		boo = unicode(foo).encode('utf8')
	return boo

API_KEY = "AIzaSyB6x36wpibEnXKP8EoKu50vniEO3dEcNDo"


# USAGE LIKE: python geocode.py -i ../raw/clean_polski.csv -o ../raw/geocoded_polski.csv -r 2712
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required = True, help = "Path to the input file")
ap.add_argument("-o", "--output", required = True, help = "Path to the output file")
ap.add_argument("-r", "--fromrow", required = True, help = "From which row to start again?")

args = vars(ap.parse_args())

csvfile = args["input"]
outputfile = args["output"]
rownum = args["fromrow"]

counter = 0

with open(csvfile, 'rb') as fin, open(outputfile, 'wb') as fout:
	reader = csv.reader(fin, delimiter=",", lineterminator='\n')
	writer = csv.writer(fout, lineterminator='\n')
	#writer.writerow(next(reader) + ["county", "city_name", "postal_code", "address", "lat_coords", "long_coords"])
	writer.writerow(next(reader) + ["county", "city_name", "postal_code", "lat_coords", "long_coords"])
	for i, row in enumerate(reader):
		if i >= int(rownum):
			geocoding_state = row[-1]
			if geocoding_state == "None":
				country = row[-2]
				county = "N/A"
				city_name = "N/A"
				postal_code = "N/A"
				#address = "N/A"
				lat_coords = "N/A"
				long_coords = "N/A"
				organization = row[1]
				PLACES_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="+organization+" "+country+"&key="+API_KEY
				r = requests.get(PLACES_URL)
				result_zero = json.loads(r.content)
				
				print json.dumps(result_zero)
				if result_zero["status"] == "OK" or result_zero["status"] == "ZERO_RESULTS":
					if len(result_zero["results"]) > 0:
						address =  result_zero["results"][0]["formatted_address"]
						GEOCODE_URL = 'https://maps.googleapis.com/maps/api/geocode/json?address='+address+'&key='+API_KEY
						r2 = requests.get(GEOCODE_URL)
						result_one = json.loads(r2.content)
						print json.dumps(result_one)
						if len(result_one["results"]) > 0:
							lat_coords = result_one['results'][0]['geometry']['location']['lat']
							long_coords = result_one['results'][0]['geometry']['location']['lng']
							for i in result_one["results"][0]["address_components"]:
								if i["types"][0] == u"postal_town":
									city_name = i["long_name"]
								if i["types"][0] == u"postal_code":
									postal_code = i["long_name"]
								if i["types"][0] == u"administrative_area_level_2":
									county = i["long_name"]
								#if i["types"][0] == u"street_address":
									#address = i["formatted_address"]
						#writer.writerow(row[:11] + ["First", uniencoder(county), uniencoder(city_name), uniencoder(postal_code), uniencoder(address), lat_coords, long_coords])
						writer.writerow(row[:11] + ["First", uniencoder(county), uniencoder(city_name), uniencoder(postal_code), lat_coords, long_coords])
						print county
						print city_name
						print postal_code
						#print address
						print lat_coords
						print long_coords
					else:
						writer.writerow(row)
					counter += 1
				else:
					if counter >= 1:
						writer.writerow(row)
						counter = 0
					else:
						break