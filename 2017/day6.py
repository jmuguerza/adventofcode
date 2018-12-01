#/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 PART 1
 Sixteen memory banks, have each an undefined number of blocks.
 The goal is to balance the blocks between the memory banks.
 The reallocation routine operates in cycles. In each cycle, finds 
 the block with the most blocks, and redistributes these blocks between
 all banks. How many redistributions can be done before a configuration
 is produced that  HAS BEEN SEEN BEFORE.
"""

INPUT = (10, 3, 15, 10, 5, 15, 5, 15, 9, 2, 5, 8, 5, 2, 3, 6)

import itertools

def redistribute(memory):
    """ Redistribute blocks of biggest memory bank """
    index = memory.index(max(memory))
    max_val = memory[index]
    memory[index] = 0
    for i in range(max_val):
        memory[(i+1+index)%len(memory)] += 1
    return memory

def count_until_repeated(memory):
    """ Count the steps before a repeated configuration is reached """
    seen = { tuple(memory) }
    for step in itertools.count():
        if len(seen) == step:
            return step
        seen.add(tuple(redistribute(memory)))

def count_distance(memory):
    """ Count the distance between two repeated states """
    seen = { tuple(memory): 0 }
    for step in itertools.count():
        if tuple(redistribute(memory)) in seen:
            return step - seen[tuple(memory)]
        seen[tuple(memory)] = step

def test(truth, check_function, *args):
    for test_input, result in truth:
        try:
            assert(check_function(test_input, *args) == result)
        except AssertionError:
            print("Error trying to assert {}({}) == {}".format(
                    check_function.__name__, test_input, result))

if __name__ == "__main__":
    # Test for PART 1
    GROUND_TRUTH = (
            ([0, 2, 7, 0], 5),
    )
    test(GROUND_TRUTH, count_until_repeated)
    # Test for PART 2
    GROUND_TRUTH = (
            ([0, 2, 7, 0], 4),
    )
    test(GROUND_TRUTH, count_distance)
    # RUN
    print('PART 1 result: {}'.format(count_until_repeated(list(INPUT))))
    print('PART 2 result: {}'.format(count_distance(list(INPUT))))
