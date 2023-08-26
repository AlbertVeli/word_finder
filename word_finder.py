#!/usr/bin/env python3

import sys
import gzip
from itertools import permutations
import multiprocessing

alphabet = list('abcdeéfghijklmnopqrstuvwxyzåäö')

# Use one array per starting letter to speed up search a bit
sys.stdout.write('Building wordlist...')
wl = {}
for c in alphabet:
    wl[c] = []
wordlist = 'dict/svenska.gz'
with gzip.open(wordlist, 'rt') as f:
    for line in f:
        first = line[0]
        wl[first].append(line.rstrip())
print('done')

# Only print once. A word like 'papegoja' will
# be printed twice because the first and second p
# are treated as individual characters. If we call
# them p(1) and p(2) the word can be written as:
# p(1)ap(2)egoja or p(2)ap(1)egoja.
printed = []

# Try one permutation
def try_one(perm):
    candidate = ''.join(perm)
    first = candidate[0]
    if candidate in wl[first]:
        if not candidate in printed:
            print(candidate)
            printed.append(candidate)

# Use multiprocessing to call try_one()
# on all CPU-cores in parallell
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f'Usage {sys.argv[0]} <letters> <number of letters in word>')
        exit(1)
    letters = list(sys.argv[1])
    num = int(sys.argv[2])
    try:
        with multiprocessing.Pool() as pool:
            pool.map(try_one, permutations(letters, num))
    except:
        pool.close()
        pool.join()
