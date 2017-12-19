#/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 PART 1
 Programs are connected by bidirectional pipes. Get the
 number of programs that are connected to 0.
 PART 2
 Get total number of groups.
"""

from functools import reduce
from collections import defaultdict

def load_and_run(filename, func):
    """ Load the file and run the function """
    with open(filename) as f:
        return func(f.read().rstrip())

def pipes_iterator(pipes_text):
    """ Iterate over pipes """
    for pipes in pipes_text.split('\n'):
        pair = pipes.split(' <-> ')
        yield from ((int(pair[0]), int(x)) for x in pair[1].split(','))

def get_number_connected_to_zero(pipes):
    """ Get the number of programs connected to zero """
    groups = defaultdict(tuple)
    # Parse text
    for prog_a, prog_b in pipes_iterator(pipes):
        progs = {prog_a, prog_b} | set(groups[prog_a]) | set(groups[prog_b])
        group = {prog_a, prog_b}
        list(map(group.update, (groups[prog] for prog in progs)))
        groups.update({ prog: tuple(group) for prog in progs })
    return len(groups[0])

def get_number_of_groups(pipes):
    """ Get the number of groups """
    groups = defaultdict(tuple)
    # Parse text
    for prog_a, prog_b in pipes_iterator(pipes):
        progs = {prog_a, prog_b} | set(groups[prog_a]) | set(groups[prog_b])
        group = {prog_a, prog_b}
        list(map(group.update, (groups[prog] for prog in progs)))
        groups.update({ prog: tuple(group) for prog in progs })
    return len(set(groups.values()))

def test(truth, check_function, *args):
    for test_input, result in truth:
        try:
            my_result = check_function(test_input, *args)
            assert(my_result == result)
        except AssertionError:
            print("Error trying to assert {}({}) = {} != {}".format(
                    check_function.__name__, test_input, my_result, result))

if __name__ == "__main__":
    # Test for PART 1
    GROUND_TRUTH = (
            ('day12_test.txt', 6),
    )
    test(GROUND_TRUTH, load_and_run, get_number_connected_to_zero)
    # Test for PART 2
    GROUND_TRUTH = (
            ('day12_test.txt', 2),
    )
    test(GROUND_TRUTH, load_and_run, get_number_of_groups)
    # RUN
    print('PART 1 result: {}'.format(load_and_run('day12.txt', get_number_connected_to_zero)))
    print('PART 2 result: {}'.format(load_and_run('day12.txt', get_number_of_groups)))
