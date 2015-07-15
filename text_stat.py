#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import argparse
import os
import string


from collections import Counter, OrderedDict

g_SEP = '-'*100
g_TOP_LETTERS  = 'E T A O I N S H R D L U'

g_TOP_WORDS = {
      0: ''
    , 1: ''
    , 2: 'of to in it is be as at so we he by or on do'
    , 3: 'the and for are but not you all'
    , 4: 'that with from this'
    }

g_LETTER_FREQ_STAT = {
    (2, False): 'Top digraphs: th er on an re he in ed nd ha at en es of \n'
    , (2, True): 'Top doubles: ss ee tt ff ll mm oo \n'
}


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
    print('Whole alphabet is: %s     (Lengh: %d)' % (printable_keys, len(keys)))
    print(g_SEP)

    without_whitespaces = [k for k in keys if k not in string.whitespace]
    print('Without whitespaces: %s     (Lengh: %d)' %
          (' '.join(without_whitespaces), len(without_whitespaces)))
    print(g_SEP)

    without_punct = [k for k in without_whitespaces if k not in string.punctuation]
    print('Without punctuation: %s     (Length: %d)' %
          (' '.join(without_punct), len(without_punct)))
    print(g_SEP)

    # print percents
    print('\n\t\tLETTERS DISTRIBUTION: \n')
    print('Most frequent letters: ' + g_TOP_LETTERS + '\n')

    for char, count in ctr.most_common():
        percent = (float(count)/data_len)*100

        if char == '\n':
            char = '\\n'
        print("{0}: {1:.2f}% ({2} times)".format(char, percent, count))
    return ctr.most_common()


def print_words_stats(data):
    print(g_SEP)
    print('\n\t\tWORDS STATISTICS: \n')
    print()

    words = data.split(' ')
    if len(words) < 3:
        print('[-] Too few words to count!')
        return

    most_common = Counter(words).most_common()
    most_common = sorted(most_common, key=lambda x: len(x[0]))
    most_common = [ (k,v) for k,v in most_common if v > 1]

    prev_word_len = len(most_common[0])
    for word, count in most_common:
        if len(word) != prev_word_len:
            print('-'*50)
            print('\nTOP %d-L words:  %s' % (len(word), g_TOP_WORDS[len(word)]))
            prev_word_len = len(word)

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
    print(g_LETTER_FREQ_STAT[(letters_count, count_same_letters)])

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
    # print_letters_stats2(data, 3)

    COUNT_SAME = True
    print_letters_stats2(data, 2, COUNT_SAME)


if __name__ == '__main__':
    main()

