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

with SqliteDict('./my_db.sqlite') as mydict:
	for key in mydict:
		print key
		print mydict[key]