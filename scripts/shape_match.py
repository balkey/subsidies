#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import json
import requests
import csv, codecs
import sys
import time
import argparse

from fuzzywuzzy import fuzz

def uniencoder(foo):
	if isinstance(foo,basestring):
		boo = foo.encode('utf8')
	else:
		boo = unicode(foo).encode('utf8')
	return boo

ap = argparse.ArgumentParser()

ap.add_argument("-i", "--input", required = True, help = "Path to the input file")
#ap.add_argument("-m", "--municipalities", required = True, help = "Path to the municipalities file")

args = vars(ap.parse_args())

csvfile = args["input"]
#munips = args["municipalities"]

municipalities = []

'''with open(munips, 'rU') as fin:
	reader = csv.reader(fin, delimiter=",", dialect=csv.excel_tab)
	for row in reader:
		municipalities.append(json.dumps(row[0]))'''


with open('../data/spatial/poland/geojson/small/gminy.json', 'r') as infile:
    data = json.load(infile)

for i in data["features"]:
	municipalities.append(json.dumps(i["properties"]["JPT_NAZWA_"]))


dist_municipalities = list(set(municipalities))

print len(dist_municipalities)

dist_municipalities = list(set(municipalities))

print len(dist_municipalities)

population = []

with open(csvfile, 'rU') as fin:
	reader = csv.reader(fin, delimiter=",", dialect=csv.excel_tab)
	for row in reader:
		population.append(json.dumps(row[5]))

dist_population = list(set(population))

print len(dist_population)

good_counter = 0
ok_counter = 0
bad_counter = 0

for i in dist_population:
	if i in dist_municipalities:
		good_counter +=1
	else:
		for z in dist_municipalities:
			if fuzz.ratio(i, z) >=70:
				ok_counter += 1
				print i, z


print good_counter
print ok_counter