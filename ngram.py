#!/usr/bin/env python
import sys

def n_gram(target, n):
    return [ target[idx:idx + n] for idx in range(len(target) - n + 1)]

target = input()
for i in n_gram(target, int(sys.argv[1])):
    print(i)
