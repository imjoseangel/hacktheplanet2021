#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import pandas as pd


def main():
    data = pd.read_csv('MLW_Data.csv', encoding="ISO-8859-1")
    print(data.to_json())


if __name__ == '__main__':
    main()
