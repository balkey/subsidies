#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import json
import requests
import csv, codecs
import sys
import time
import argparse

from sqlitedict import SqliteDict

#mydict = SqliteDict('./my_db.sqlite', autocommit=True)

def geocode_address(results):
	county = "N/A"
	city_name = "N/A"
	postal_code = "N/A"
	address = "N/A"
	lat_coords = "N/A"
	long_coords = "N/A"
	address =  results["results"][0]["formatted_address"]
	GEOCODE_URL = 'https://maps.googleapis.com/maps/api/geocode/json?address='+address+'&key='+API_KEY[rounds]
	r2 = requests.get(GEOCODE_URL)
	result_one = json.loads(r2.content)
	print json.dumps(result_one)
	if result_one["results"]:
		lat_coords = result_one['results'][0]['geometry']['location']['lat']
		long_coords = result_one['results'][0]['geometry']['location']['lng']
		for i in result_one["results"][0]["address_components"]:
			if i["types"][0] == u"postal_town":
				city_name = i["long_name"]
			if i["types"][0] == u"postal_code":
				postal_code = i["long_name"]
			if i["types"][0] == u"administrative_area_level_2":
				county = i["long_name"]
			if i["types"][0] == u"street_address":
				address = i["formatted_address"]
	mydict[company] = ["First", uniencoder(county), uniencoder(city_name), uniencoder(postal_code), uniencoder(address), lat_coords, long_coords]

def uniencoder(foo):
	if isinstance(foo,basestring):
		boo = foo.encode('utf8')
	else:
		boo = unicode(foo).encode('utf8')
	return boo

API_KEY = ["AIzaSyB6x36wpibEnXKP8EoKu50vniEO3dEcNDo", "AIzaSyAXt42jURuoixnkHuoRHI7G-8gBznqMjkM", "AIzaSyDVctzdm79NIz3e0C1nEdrczNCYbi5Z4CE"]
rounds = 0

# USAGE LIKE: python geocode.py -i ../raw/clean_polski.csv -o ../raw/geocoded_polski.csv -r 2712
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required = True, help = "Path to the input file")
ap.add_argument("-o", "--output", required = True, help = "Path to the output file")
ap.add_argument("-c", "--country", required = True, help = "Country to be geocoded")
#ap.add_argument("-r", "--fromrow", required = True, help = "From which row to start again?")

args = vars(ap.parse_args())

csvfile = args["input"]
outputfile = args["output"]
country = args["country"]
#rownum = args["fromrow"]

beneficiaries = {}

with open(csvfile, 'rb') as fin_count:
	reader = csv.reader(fin_count, delimiter=",", lineterminator='\n')
	for row in reader:
		if row[7] in beneficiaries:
			beneficiaries[row[7]]["variations"].append(row[1])
		else:
			beneficiaries[row[7]] = {"variations": [row[1]]}


for ids in beneficiaries:
	beneficiaries[ids]["variations"] = list(set(beneficiaries[ids]["variations"]))

counter_a = 0
counter_l = 0

with SqliteDict('./my_db.sqlite') as mydict:
	for company in beneficiaries:
		if company not in mydict.keys():
			PLACES_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="+company+" "+country+"&key="+API_KEY[rounds]
			r = requests.get(PLACES_URL)
			result_zero = json.loads(r.content)
			print json.dumps(result_zero)
			if result_zero["status"] == "OK" or result_zero["status"] == "ZERO_RESULTS":
				if len(result_zero["results"]) > 0:
					geocode_address(result_zero)
					counter_a += 1
					counter_l += 1
					#writer.writerow(row[:11] + ["First", uniencoder(county), uniencoder(city_name), uniencoder(postal_code), lat_coords, long_coords])
					#print county
					#print city_name
					#print postal_code
					#print address
					#print lat_coords
					#print long_coords
				else:
					for i in beneficiaries[company]["variations"]:
				 		PLACES_URL_v = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="+i+" "+country+"&key="+API_KEY[rounds]
				 		r_v = requests.get(PLACES_URL_v)
						result_zero_v = json.loads(r_v.content)
						if len(result_zero_v["results"]) > 0:
							geocode_address(result_zero_v)
							counter_a += 1
							counter_l += 1
							break
						if beneficiaries[company]["variations"].index(i) == len(beneficiaries[company]["variations"]) - 1:
							for i in beneficiaries[company]["variations"]:
								PLACES_URL_v2 = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="+i+"&key="+API_KEY[rounds]
								r_v2 = requests.get(PLACES_URL_v2)
								result_zero_v2 = json.loads(r_v2.content)
								if len(result_zero_v2["results"]) > 0:
									geocode_address(result_zero_v2)
									counter_a += 1
									counter_l += 1
									break
								if beneficiaries[company]["variations"].index(i) == len(beneficiaries[company]["variations"]) - 1:
									county = "N/A"
									city_name = "N/A"
									postal_code = "N/A"
									address = "N/A"
									lat_coords = "N/A"
									long_coords = "N/A"
									mydict[company] = ["First", uniencoder(county), uniencoder(city_name), uniencoder(postal_code), uniencoder(address), lat_coords, long_coords]
									counter_a += 1
									counter_l += 1
						
			else:
				if counter_l >= 1:
					county = "N/A"
					city_name = "N/A"
					postal_code = "N/A"
					address = "N/A"
					lat_coords = "N/A"
					long_coords = "N/A"
					mydict[company] = ["First", uniencoder(county), uniencoder(city_name), uniencoder(postal_code), uniencoder(address), lat_coords, long_coords]
					counter_l = 0
				else:
					if rounds < 2:
						rounds += 1
					else:
						break
			print counter_a
			mydict.commit()