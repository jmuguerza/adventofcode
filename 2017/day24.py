#/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 PART 1
 We have to build a bridge out of components, each with two ports
 (one on each end). Only matching types can be connected. The input
 shows the type of ports, the two numbers indicating the number
 of pins on each port. You start with a 0-pin connector. The goal
 is to build the strongest bridge possible (strength measured as the
 sum of all ports).
 PART 2
 Get the strength of the longest bridge.
"""

import sys

def add_component(bridge, component):
    """ Add component to a bridge """
    return bridge + list(sorted(component, key=lambda x: x!= bridge[-1]))

def build_bridges(components, bridge=[0,]):
    """ Build all possible bridges """
    for i, component in enumerate(components):
        if bridge[-1] not in component:
            continue
        yield from build_bridges(
                tuple(components[n] for n in range(len(components)) if n != i),
                add_component(bridge, component))
    yield bridge

def get_strongest(lines):
    """ Get strongest bridge """
    components = list( tuple(map(int, line.split('/'))) for line in lines )
    return sum(max(build_bridges(components), key=sum))

def get_longest(lines):
    """ Get the strongest amonst the longest of bridges """
    components = list( tuple(map(int, line.split('/'))) for line in lines )
    longest_length = 0
    longest_bridges = []
    for bridge in build_bridges(components):
        if len(bridge) > longest_length:
            longest_length = len(bridge)
            longest_bridges = [bridge]
        elif len(bridge) == longest_length:
            longest_bridges.append(bridge)
    return sum(max(longest_bridges, key=sum))

def load_and_run(filename, func, *args):
    """ Load the file and run the function """
    with open(filename) as f:
        lines = f.read().splitlines()
    return func(lines, *args)

def test(truth, check_function, *args):
    for test_input, expected_result in truth:
        try:
            result = check_function(test_input, *args)
            assert(result == expected_result)
        except AssertionError:
            print("Error trying to assert {}({}) = {} == {} ".format(
                    check_function.__name__, test_input, result, expected_result))
            sys.exit(1)

if __name__ == "__main__":
    # Test for PART 1
    GROUND_TRUTH = (('day24_test.txt', 31),)
    test(GROUND_TRUTH, load_and_run, get_strongest)
    # Test for PART 2
    GROUND_TRUTH = (('day24_test.txt', 19),)
    test(GROUND_TRUTH, load_and_run, get_longest)
    # RUN
    print('PART 1 result: {}'.format(load_and_run('day24.txt', get_strongest)))
    print('PART 2 result: {}'.format(load_and_run('day24.txt', get_longest)))
