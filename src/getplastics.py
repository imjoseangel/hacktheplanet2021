#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import re
import requests


def main():

    response = requests.get(
        'http://fme.discomap.eea.europa.eu/fmedatadownload/MarineLitter/MLWPivotExport.fmw'
        '?CommunityCode=&FromDate=2010-01-01&ToDate=2022-12-31'
        '&opt_showresult=false&opt_servicemode=sync')

    downloadlink = re.search(
        r"<a\s+(?:[^>]*?\s+)?href=([\"'])(.*?)\1>", response.content.decode()).group(2)

    zipfile = requests.get(downloadlink)
    open('fme.zip', 'wb').write(zipfile.content)


if __name__ == '__main__':
    main()
