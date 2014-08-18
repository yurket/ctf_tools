#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function

import string
import sys


def create_stat_dict():
    chars = {
          'digits': 0
        , 'asciis': 0
        , 'punct': 0
        , 'whitespace': 0
    }
    return chars


if __name__ == "__main__":
    for line in sys.stdin:

        stat = create_stat_dict()
        for c in line:
            if c in string.digits:
                stat['digits'] += 1
            elif c in string.ascii_letters:
                stat['asciis'] += 1
            elif c in string.punctuation:
                stat['punct'] += 1
            elif c in string.whitespace:
                stat['whitespace'] += 1
            else:
                pass
        l = len(line)
        punct_percent = (stat['punct'] / float(l)) * 100
        if punct_percent > 30:
            continue
        # print('%s  [%f]' % (line, punct_percent))
        print(line, end='')


