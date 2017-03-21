#!/usr/bin/python
# -*- coding: utf-8 -*-


import csv
import json
import requests
import csv, codecs
import sys
import time
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required = True, help = "Path to the input file")

args = vars(ap.parse_args())

csv.register_dialect(
    'mydialect',
    delimiter = ',',
    quotechar = '"',
    doublequote = True,
    skipinitialspace = True,
    lineterminator = '\r\n',
    #quoting = csv.QUOTE_ALL
    quoting = csv.QUOTE_NONNUMERIC)

csvfile = args["input"]

beneficiaries = []
empty_counter = 0

with open(csvfile, 'rb') as fin:
	reader = csv.reader(fin, delimiter=",", lineterminator='\n')
	counter = 0
	for row in reader:
		counter +=1
		if row[14]:
			beneficiaries.append(row[14])
		else:
			empty_counter += 1



dist_beneficiaries = list(set(beneficiaries))

print len(dist_beneficiaries)
print empty_counter
print counter