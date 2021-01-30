#!/usr/bin/env python3

import timeit
import random
import re

# a test set is (input size, number of trials)
test_sets = [(1, 1000000), (10, 1000000), (100, 100000), (500, 100000),
             (1000, 10000), (10000, 1000), (25000, 1000), (50000, 500)] 
MIN_STR_SZ = 5
MAX_STR_SZ = 100

rx = r'^.*(?<!hello)\s+(WORLD)(?!hello)([!]*)$'

def test_re_comp(strings):
    rv = []
    rxc = re.compile(rx)
    for idx, x in enumerate(strings):
        if rxc.match(x):
            rv.append((idx, rxc.sub(r'\1\2', x)))
    return rv

def test_re_no_comp(strings):
    rv = []
    for idx, x in enumerate(strings):
        if re.match(rx, x):
            rv.append((idx, re.sub(rx, r'\1\2', x)))
    return rv

# make a list of alpha-numerics and then use it to build random strings:
# STR_CT number of strings of lengths between MIN_STR_SZ and MAX_STR_SIZE
ltr =  [chr(x) for x in (*range(65, 91), *range(97, 123), 33)]
strings = [''.join(random.choices(ltr, k=random.randint(MIN_STR_SZ, MAX_STR_SZ)))
           for _ in range(max(x[0] for x in test_sets))]

for test_set in test_sets:
    sample = random.sample(strings, test_set[0])
    comp = timeit.timeit("test_re_comp(strings)", number=test_set[1],
                         globals={'strings': sample,
                                  'test_re_comp': test_re_comp})
    no_comp = timeit.timeit("test_re_no_comp(strings)", number=test_set[1],
                            globals={'strings': sample,
                                     'test_re_no_comp': test_re_no_comp})
    print(f'\n{test_set[0]} strings, {test_set[1]} executions\n{"-"*40}')
    print(f'pre-compiled: {comp}\nnot pre-compiled: {no_comp}\n')
    print(f'Diff: {abs(comp-no_comp)}, %: {(abs(comp-no_comp)/comp)*100}\n')

