#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import argparse
import os
import string


from collections import Counter, OrderedDict

g_SEP = '-'*100


def print_letters_stats(data):
    if not data:
        print('Empty data')
        return None

    data_len = len(data)
    ctr = Counter(data)

    print('\n\t\t\tSTATISTICS:')
    print(g_SEP)
    print()
    keys = sorted(ctr.keys())
    printable_keys = (' '.join(keys)).replace('\n', '\\n')
    print('Whole alphabet is: %s' % printable_keys)
    print('Lengh: %d' % len(keys))
    print(g_SEP)

    without_whitespaces = [k for k in keys if k not in string.whitespace]
    print('Without whitespaces: %s' % ' '.join(without_whitespaces))
    print('Lengh: %d' % len(without_whitespaces))
    print(g_SEP)

    without_punct = [k for k in without_whitespaces if k not in string.punctuation]
    print('Without punctuation: %s' % ' '.join(without_punct))
    print('Lengh: %d' % len(without_punct))
    print(g_SEP)

    # print percents
    print('\n\t\tLETTERS DISTRIBUTION: \n')
    for char, count in ctr.most_common():
        percent = (float(count)/data_len)*100

        if char == '\n':
            char = '\\n'
        print("{0}: {1:.2f}% ({2} times)".format(char, percent, count))

    return ctr.most_common()


def print_words_stats(data):
    print(g_SEP)
    print('\n\t\tWORDS STATISTICS: \n')

    words = data.split(' ')
    if len(words) < 3:
        print('[-] Too few words to count!')
        return

    most_common = Counter(words).most_common()
    for word, count in most_common:
        percent = (float(count)/len(words))*100
        print("{0}: {1:.2f}% ({2} times)".format(word, percent, count))

    return most_common


def print_letters_stats2(data, letters_count, count_same_letters=False):
    '''
        Prints 10 most frequent sequences of letters of
        *letters_count* length
    '''
    print(g_SEP)
    print_str = '(repeated letters)' if count_same_letters else ''
    print('\n\t\t%d-GRAPHS %s STATISTICS: \n' % (letters_count, print_str))

    letters_map = {}
    for i in xrange(len(data)-letters_count+1):
        key = data[i:i+letters_count]
        if ' ' in key:
            continue

        if count_same_letters and key.count(key[0]) != letters_count:
            continue

        if key not in letters_map.keys():
            letters_map[key] = 1
        else:
            letters_map[key] = letters_map[key] + 1

    sorted_letters_map = OrderedDict(
        sorted(letters_map.items(), key=lambda x: x[1], reverse=True))

    for k,v in sorted_letters_map.items()[:10]:
        print(k,v)


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

    print_letters_stats(data)
    print_words_stats(data)

    print_letters_stats2(data, 2)
    print_letters_stats2(data, 3)

    COUNT_SAME = True
    print_letters_stats2(data, 2, COUNT_SAME)


if __name__ == '__main__':
    main()

