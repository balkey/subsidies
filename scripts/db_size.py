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

mydict = SqliteDict('./my_db.sqlite', autocommit=True)


print len(mydict.keys())