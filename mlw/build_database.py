#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import logging
import os
import pandas as pd
import re
import requests
import sqlite3
import sys
from zipfile import ZipFile
from config import db
from models import MarinaLitterWatch


# Set Logging
logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s",
                    datefmt="%d-%b-%y %H:%M:%S", stream=sys.stdout, level=logging.INFO)

# Download data
logging.info("Downloading data...")
response = requests.get(
    'http://fme.discomap.eea.europa.eu/fmedatadownload/MarineLitter/MLWPivotExport.fmw'
    '?CommunityCode=&FromDate=2010-01-01&ToDate=2022-12-31'
    '&opt_showresult=false&opt_servicemode=sync')

downloadlink = re.search(
    r"<a\s+(?:[^>]*?\s+)?href=([\"'])(.*?)\1>", response.content.decode()).group(2)

logging.info("Saving data...")
zipfile = requests.get(downloadlink)
open('fme.zip', 'wb').write(zipfile.content)

logging.info("Uzipping data...")
zipObject = ZipFile('fme.zip', 'r')
zipObject.extractall()

logging.info("Loading data...")
# Data to initialize database with
data = pd.read_csv('CSV_1/MLW_PivotExport/MLW_Data.csv', encoding="ISO-8859-1")

# Delete database file if it exists currently
if os.path.exists("mlw.db"):
    os.remove("mlw.db")

# Create the database
db.create_all()

# populate the database
conn = sqlite3.connect('mlw.db')
data.to_sql('mlw', conn, if_exists='append')

db.session.commit()
