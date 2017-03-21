#!/usr/bin/python
# -*- coding: utf-8 -*-


import csv
import json
import requests
import csv, codecs
import sys
import time
import argparse
import random

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required = True, help = "Path to the input file")
ap.add_argument("-o", "--output", required = True, help = "Path to the output file")

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
outputfile = args["output"]

lines_to_grab = random.sample(xrange(2727245), 1000)

uniques = []

with open(csvfile, 'rb') as fin, open(outputfile, 'wb') as fout:
	reader = csv.reader(fin, delimiter=",", lineterminator='\n')
	writer = csv.writer(fout, dialect="mydialect")
	for i, line in enumerate(reader):
		new_row = []
		if i in lines_to_grab:
			if line[14] not in uniques:
				new_row.append(line[14])
				new_row.append(line[1])
				new_row.append(line[12])
				uniques.append(line[14])
				writer.writerow(new_row)
	