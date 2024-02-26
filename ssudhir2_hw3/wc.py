#!/usr/bin/env python3

import sys

def count_chars(string): # 3 (1.)

    if not isinstance(string, (str, )):
        raise TypeError(f'string = {string} should be of type str.')

    return len(string)


def count_words(string): # 3 (2.)

    if not isinstance(string, (str, )):
        raise TypeError(f'string = {string} should be of type str.')

    return len(string.split())


if (len(sys.argv) - 1) != 1:
    raise TypeError(f'Expected 1 command line arguement (filename), got {len(sys.argv) - 1} instead.')

filename = sys.argv[1] # 3 (3.)
with open(filename, 'r') as f:
    num_lines = 0
    num_words = 0
    num_chars = 0
    for line in f:
        num_lines += 1
        num_chars += count_chars(line)
        num_words += count_words(line)

print(num_lines)
print(num_words)
print(num_chars)
print(filename)