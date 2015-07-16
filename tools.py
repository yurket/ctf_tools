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



def xor_bytes(a, b):
    if len(a) != len(b):
        print('[!] strings of different length!')
    if len(a) > len(b):
        return "".join([chr(x^y) for (x,y) in zip(a[:len(b)], b)]).encode('hex')
    else:
        return "".join([chr(x^y) for (x,y) in zip(a, b[:len(a)])]).encode('hex')

def xor_strings(a, b):
    return bytexor(string_to_bytes(a), string_to_bytes(b))

def xor_hexs(a, b):
    return bytexor(hex_to_bytes(a), hex_to_bytes(b))


def main():
    pass


if __name__ == '__main__':
    main()

