#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import datetime as dt
from glob import glob
import logging
import os
from os.path import abspath, dirname, normpath
import pandas as pd
import re
import requests
from shutil import rmtree
import sqlite3
import sys
from zipfile import ZipFile
from config import db
from models import MarinaLitterWatch

CLEAN_FILES = ('./CSV_1', './CSV_2')
ZIP_FILE = 'fme.zip'
DB_FILE = 'mlw.db'

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
open(ZIP_FILE, 'wb').write(zipfile.content)

logging.info("Uzipping data...")
zipObject = ZipFile(ZIP_FILE, 'r')
zipObject.extractall()

logging.info("Loading data...")
# Data to initialize database with
data = pd.read_csv('CSV_1/MLW_PivotExport/MLW_Data.csv',
                   encoding="ISO-8859-1", parse_dates=['EventDate'])

data['EventDate'] = (data['EventDate'] -
                     dt.datetime(1970, 1, 1)).dt.total_seconds()

# Delete database file if it exists currently
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

# Create the database
db.create_all()

# populate the database
conn = sqlite3.connect(DB_FILE)
data.to_sql('mlw', conn, if_exists='append')

db.session.commit()

# Clean files
logging.info("Cleaning files...")

here = normpath(abspath(dirname(__file__)))

for path_spec in CLEAN_FILES:
    # Make paths absolute and relative to this path
    abs_paths = glob(os.path.normpath(
        os.path.join(here, path_spec)))
    for path in [str(p) for p in abs_paths]:
        if not path.startswith(here):
            # Die if path in CLEAN_FILES is absolute + outside this directory
            raise ValueError(
                "%s is not a path inside %s" % (path, here))
        logging.info(f'removing {os.path.relpath(path)}')
        rmtree(path)

logging.info(f'removing {ZIP_FILE}')
os.remove(ZIP_FILE)
