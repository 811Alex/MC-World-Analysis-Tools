#!/usr/bin/env python3

from sys import stderr

max_reprint_len = 0

def reprint(val):
    global max_reprint_len
    print('\r' + val.ljust(max_reprint_len, ' '), end='')
    if len(val) > max_reprint_len:
        max_reprint_len = len(val)

def error(err):
    print(err, file=stderr)
