#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import requests
import json
import gzip
import os
from config import cache
from models import MarinaLitterWatch, MarinaLitterWatchSchema
from flask_sqlalchemy_caching import FromCache


def send_all(account, apikey):
    """
    This function sends data to new relic
    with the complete lists of items

    :return:        content body
    """
    # Create the list of items from our data
    mlw = MarinaLitterWatch.query.order_by(
        MarinaLitterWatch.communityname).options(FromCache(cache)).all()

    # Serialize the data for the response
    mlw_schema = MarinaLitterWatchSchema(many=True)
    data = mlw_schema.dump(mlw)

    # Send data to New Relic
    json_data = json.dumps(data, indent=2)
    encoded = json_data.encode('utf-8')
    compressed = gzip.compress(encoded)
    custom_header = {"Content-Type": "application/json",
                     "X-Insert-Key": apikey, "Content-Encoding": "gzip"}
    send_data = requests.post(f"https://insights-collector.newrelic.com/v1/accounts/{account}/events",
                              data=compressed, headers=custom_header)

    return send_data.content, send_data.status_code


def main():
    nrapikey = os.environ['NR_API']
    nraccount = os.environ['NR_ACCOUNT']
    run = send_all(account=nraccount, apikey=nrapikey)
    print(run)


if __name__ == '__main__':
    main()
