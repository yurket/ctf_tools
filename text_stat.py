#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import argparse
import os
import string
import sys

from collections import Counter, OrderedDict

# frequency statistics taken from here:
# http://www.macfreek.nl/memory/Letter_Distribution

g_SEP = '-'*100
g_TOP_LETTERS  = 'E T A O I N S H R D L U'

g_TOP_WORDS = [
      (1, 'a I')
    , (2, 'of to in it is be as at so we he by or on do')
    , (3, 'the and for are but not you all')
    , (4, 'that with from this')
    ]

g_LETTER_FREQ_STAT = {
      (2, False): 'Top digraphs: th er on an re he in ed nd ha at en es of \n'
    , (2, True): 'Top doubles: ss ee tt ff ll mm oo \n'
}


def IS_PYTHON3():
    return sys.version_info.major == 3


def replace_not_printable_with_hex(ch):
    if ch not in string.printable:
        return '{:02x}'.format(ch)
    if ch == ord('\n'):
        return '\\n'
    elif ch == ord('\t'):
        return '\\t'
    elif ch == ord('\x0b'):
        return '\\b'
    elif ch == ord('\x0c'):
        return '\\c'
    elif ch == ord('\r'):
        return '\\r'
    return ch


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
    most_common = ctr.most_common()

    all_alphabet = [ replace_not_printable_with_hex(k) for k in keys ]
    all_alphabet = (' '.join(all_alphabet))
    print('All alphabet is: %s     (Lengh: %d)' % (all_alphabet, len(keys)))
    print(g_SEP)

    without_whitespaces = [k for k in keys if k not in string.whitespace]
    without_whitespaces = [replace_not_printable_with_hex(c) for c in without_whitespaces]
    print('Without whitespaces: %s     (Lengh: %d)' %
          (' '.join(without_whitespaces), len(without_whitespaces)))
    print(g_SEP)

    without_punct = [k for k in without_whitespaces if k not in string.punctuation]
    print('Without punctuation: %s     (Length: %d)' %
          (' '.join(without_punct), len(without_punct)))
    print(g_SEP)

    print('\n\t\tLETTERS DISTRIBUTION: \n')
    print('Most frequent letters: ' + g_TOP_LETTERS + '\n')

    for char, count in most_common[:50]:
        percent = (float(count)/data_len)*100

        char = replace_not_printable_with_hex(char)
        print("{0}: {1:.2f}% ({2} times)".format(char, percent, count))
    return most_common


def print_words_stats(data):
    print(g_SEP)
    print('\n\t\tWORDS STATISTICS: \n')
    print()

    words = str(data).split(' ')
    if len(words) < 3:
        print('[-] Too few words to count!')
        return

    most_common = Counter(words).most_common()
    # sort by words length
    most_common = sorted(most_common, key=lambda x: len(x[0]))
    most_common = [ (k,v) for k,v in most_common if v > 1]
    if not len(most_common):
        print("Nothing to show about words")
        return []

    for reference_word_length, message in g_TOP_WORDS:
        print('-'*50)
        print('\nTOP %d-L words:  %s' % (reference_word_length, message))
        for word, word_count in most_common:
            if len(word) != reference_word_length:
                continue
            percent = (float(word_count)/len(words))*100
            print("{0}: {1:.2f}% ({2} times)".format(word, percent, word_count))

    return most_common


def print_letters_analysis(data, letters_count, count_same_letters=False):
    '''
        Prints 10 most frequent sequences of letters of
        *letters_count* length
    '''
    print(g_SEP)
    print_str = '(repeated letters)' if count_same_letters else ''
    print('\n\t\t%d-GRAPHS %s STATISTICS: \n' % (letters_count, print_str))
    print(g_LETTER_FREQ_STAT[(letters_count, count_same_letters)])

    letters_map = {}
    for i in range(len(data)-letters_count+1):
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

    for letters, count in list(sorted_letters_map.items())[:10]:
        escaped_letters = ''.join(map(replace_not_printable_with_hex, letters))
        print(escaped_letters, count)

    return sorted_letters_map


def print_most_common_first_letter(data):
    print(g_SEP)
    print('\n\t\tMOST COMMON FIRST LETTERS: \n')
    print('\nTOP first letters:  t o a w ...')
    print()

    first_letters = [word[0] for word in data.split()]
    ctr = Counter(first_letters)

    for char, count in ctr.most_common()[:4]:
        percent = (float(count)/len(first_letters))*100

        char = replace_not_printable_with_hex(char)
        print("{0}: {1:.2f}% ({2} times)".format(char, percent, count))


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

    if IS_PYTHON3():
        data = data.decode()

    print_letters_stats(data)

    print_words_stats(data)

    print_letters_analysis(data, letters_count=2)

    print_letters_analysis(data, letters_count=2, count_same_letters=True)

    print_most_common_first_letter(data)

if __name__ == '__main__':
    main()

