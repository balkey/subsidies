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

export_json = {}

with SqliteDict('./my_db.sqlite') as mydict:
	for key in mydict:
		export_json[key] = mydict[key]

with open('database_export.json', 'w') as outfile:
    json.dump(export_json, outfile)