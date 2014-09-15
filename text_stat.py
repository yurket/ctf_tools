#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import argparse
import os
import string


from collections import Counter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    filename = args.filename
    if not os.path.exists(filename):
        print('[-] Error: File %s does not exists!' % filename)
        return

    data = None
    try:
        with open(filename, 'rb') as f:
            data = f.read()
    except IOError as e:
        print(e.message)
        return

    data_len = len(data)
    ctr = Counter(data)

    # print percents
    for char, count in ctr.most_common():
        percent = (float(count)/data_len)*100
        percent = str(round(percent, 3)) + '%'

        if char == '\n':
            char = '\\n'
        print("%s: %s" %(char, percent))


if __name__ == '__main__':
    main()

