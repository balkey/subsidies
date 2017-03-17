#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import json
import requests
import csv, codecs
import sys
import time
import argparse


# USAGE LIKE: python clean.py -i ../raw/polski.csv -o ../raw/clean_polski.csv -c 0 1 2 3 6 7 12 14 26 27 -ctr Poland
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required = True, help = "Path to the input file")
ap.add_argument("-o", "--output", required = True, help = "Path to the output file")
ap.add_argument("-c", "--columns", required = True, nargs="*", help = "Provide a list of column indexes you wish to keep")
ap.add_argument("-ctr", "--country", required = True, help = "Provide a countryname you wish to add")

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
columns = args["columns"]
country = args["country"]

with open(csvfile, 'rb') as fin, open(outputfile, 'wb') as fout:
	reader = csv.reader(fin, delimiter=",", lineterminator='\n')
	#writer = csv.writer(fout, delimiter=",", quotechar='"', lineterminator='\n')
	#writer = csv.writer(fout, delimiter=",", lineterminator='\n')
	writer = csv.writer(fout, dialect="mydialect")
	#writer.writerow(next(reader) + ["Start_date", "End_date"])
	counter = 0
	for row in reader:
		new_row = []
		cellcounter = 0
		for cell in row: 
			if str(cellcounter) in columns:
				if type(cell) == int or type(cell) == float:
					new_row.append(cell)
				else:
					cell1 = str(cell).replace('"', '').strip()
					new_row.append(str(cell1))
			cellcounter += 1
		if counter == 0:
			new_row.append("country")
			new_row.append("geocoding_state")
		else:
			new_row.append(country)
			new_row.append("None")
		writer.writerow(new_row)
		counter += 1

print counter