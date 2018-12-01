#/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 PART 1
 The hashes of day 10 are used to represent the state of a disk of 128x128.
 Each hash represents the state of a row, bitwise: a 1 bit means used, 0 free.
 Given the string input, append "-<n_row>" to get the hash, and calculate
 the number of used squares.
"""


INPUT = 'xlqgujun' # The input string

from itertools import count
from functools import reduce
from contextlib import suppress

from day10 import get_hash

def to_binary(hexa):
    """ Return the binary representation of a hex string """
    return bin(int(hexa, 16))[2:].zfill(len(hexa)*4)

def get_used(string):
    """ Get the number of used squares, using input string """
    return sum(
            to_binary(get_hash('{}-{}'.format(string, row))).count('1')
            for row in range(128))

def paint_region(diskmap, row, column, color):
    """ Paint recursively a region with color """
    try:
        if row < 0 or column < 0 or diskmap[row][column] != '1':
            return
    except IndexError:
        return
    diskmap[row][column] = color
    paint_region(diskmap, row-1, column, color)
    paint_region(diskmap, row, column-1, color)
    paint_region(diskmap, row+1, column, color)
    paint_region(diskmap, row, column+1, color)

def count_regions(diskmap):
    """ Count the number of regions on the map """
    num = count(2)
    for row in range(len(diskmap)):
        while '1' in diskmap[row]:
            paint_region(diskmap, row, diskmap[row].index('1'), str(next(num)))
    return next(num)-2

def get_regions(string):
    """ Get the number of used regions """
    # Build the map
    diskmap = list(
            list(to_binary(get_hash('{}-{}'.format(string, row))))
            for row in range(128)
    )
    # Count adjacent regions
    return count_regions(diskmap)

def test(truth, check_function, *args):
    for test_input, result in truth:
        try:
            my_result = check_function(test_input, *args)
            assert(my_result == result)
        except AssertionError:
            print("Error trying to assert {}({}) == {} != {}".format(
                    check_function.__name__, test_input, my_result, result))

if __name__ == "__main__":
    # Test for PART 1
    GROUND_TRUTH = (
            ('flqrgnkx', 8108),
    )
    test(GROUND_TRUTH, get_used)
    # Test for PART 2
    GROUND_TRUTH = (
            ('flqrgnkx', 1242),
    )
    test(GROUND_TRUTH, get_regions)
    # RUN
    print('PART 1 result: {}'.format(get_used(INPUT)))
    print('PART 2 result: {}'.format(get_regions(INPUT)))
