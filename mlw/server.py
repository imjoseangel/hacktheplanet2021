#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main module of the server file
"""

from os.path import abspath, dirname, normpath
import sys
from flask import render_template
import hupper
from waitress import serve

# local modules
import config

INDEX_FILE = 'index.html'
MAP_FILE = 'locations.html'
DB_FILE = 'mlw.db'

# Set local path
here = normpath(abspath(dirname(__file__)))

# Get the application instance
connex_app = config.connex_app

# Read the swagger.yml file to configure the endpoints
connex_app.add_api("swagger.yml")

# Create a URL route in our application for "/"


@connex_app.route("/")
def home():
    """
    This function just responds to the browser URL
    localhost:8080/

    :return:        the rendered template "home.html"
    """
    return render_template("index.html")


@connex_app.route("/locations")
def locations():
    return render_template('locations.html')


def main():

    # start_reloader will only return in a monitored subprocess
    reloader = hupper.start_reloader('server.main')

    # monitor an extra file
    reloader.watch_files(
        [f'{here}/templates/{MAP_FILE}', f'{here}/templates/{INDEX_FILE}', f'{here}/{DB_FILE}'])

    # connex_app.run(debug=True)
    serve(connex_app.app)


if __name__ == '__main__':
    main()
