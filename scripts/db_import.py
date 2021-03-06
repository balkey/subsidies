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

with open('database_export.json', 'r') as outfile:
    data = json.loads(outfile)

with SqliteDict('./my_db.sqlite') as mydict:
	for key in data:
		mydict[key] = data[key]
		mydict.commit()