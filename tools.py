#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function


def string_to_bytes(s):
    return [ord(x) for x in s]

def bytes_to_string(b):
    return ''.join(chr(x) for x in b)

def string_to_hex(s):
    return s.encode('hex')

def hex_to_string(s):
    return s.decode('hex')

def bytes_to_hex(b):
    return hex_to_string(bytes_to_string(b))

def hex_to_bytes(s):
    return string_to_bytes(hex_to_string(s))

# ================================================================================

def xor_bytes(a, b):
    if len(a) != len(b):
        print('[!] strings of different length!')
    if len(a) > len(b):
        return "".join([chr(x^y) for (x,y) in zip(a[:len(b)], b)]).encode('hex')
    else:
        return "".join([chr(x^y) for (x,y) in zip(a, b[:len(a)])]).encode('hex')

def xor_strings(a, b):
    return xor_bytes(string_to_bytes(a), string_to_bytes(b))

def xor_hexs(a, b):
    return xor_bytes(hex_to_bytes(a), hex_to_bytes(b))



def repeating_xor_bytes(a, k):
    return "".join([ chr(c^k[i%len(k)]) for i,c in enumerate(a) ])

def repeating_xor_strings(a, k):
    return repeating_xor_bytes(string_to_bytes(a), string_to_bytes(k))

def repeating_xor_hexs(a, k):
    return repeating_xor_bytes(hex_to_bytes(a), hex_to_bytes(k))

# ================================================================================

from collections import Counter
import string


def is_printable_string(s):
    for c in s:
        if c not in string.printable:
            return False
    return True

def is_printable_hex(h):
    return is_printable_string(hex_to_string(h))


def single_byte_xor_cipher_breaker(ct_hex):
    """
    *ct_hex* - a ciphertext, xored with 1 byte.
    """

    # ' ' E T A O I N    S H R D L U
    MOST_COMMON_ENG = [0x20, 0x65, 0x74, 0x61, 0x6f, 0x69, 0x6e,
                       0x73, 0x68, 0x72, 0x64, 0x6c, 0x75]

    ct_bytes = hex_to_bytes(ct_hex)
    most_common_byte = Counter(ct_bytes).most_common()[0][0]

    for i, guess in enumerate(MOST_COMMON_ENG):
        key_byte = most_common_byte ^ guess
        pt_hex = xor_bytes(ct_bytes, [key_byte]*len(ct_bytes))
        if not is_printable_hex(pt_hex):
            continue
        print("guess #%d('%c') is: %s" %
              (i+1, chr(guess), hex_to_string(pt_hex)))



def main():
    pass


if __name__ == '__main__':
    main()

