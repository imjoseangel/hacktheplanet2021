#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import os
import pandas as pd
import sqlite3
from config import db
from models import MarinaLitterWatch

# Data to initialize database with
data = pd.read_csv('MLW_Data.csv', encoding="ISO-8859-1")

# Delete database file if it exists currently
if os.path.exists("mlw.db"):
    os.remove("mlw.db")

# Create the database
db.create_all()

# populate the database
conn = sqlite3.connect('mlw.db')
data.to_sql('mlw', conn, if_exists='append')

db.session.commit()
