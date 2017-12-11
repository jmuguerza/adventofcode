#/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 PART 1
 A hash is calculated by repeatedly twisting parts of a string. To achieve
 this, begin with a list of numbers from 0 to 255, a CURRENT POSITION, which
 begins at 0, a SKIP SIZE, which begins at 0, and a sequence of LENGTHS. Then,
 for each length:
 - REVERSE the order of that LENGTH of elements in the list, starting at 
   CURRENT POSITION
 - MOVE the CURRENT POSITION forward by LENGTH plus the SKIP SIZE.
 - INCREASE SKIP SIZE by 1.
 The list is circular. LENGHTS larger than the size of the list are invalid.
 Return the first two elements multiplied.
 PART 2
 Now the input is a string, and add 17, 31, 73, 47, 23. Run 64 rounds. Use the
 same lengths, but keep CURRENT POSITION and SKIP SIZE between rounds. The
 result is called SPARSE HASH. Reduce the 256 numbers to 16 numbers, called 
 DENSE HASH. Use bitwise XOR to combine each consecutive block of 16 numbers.
 Represent the hash in hexadecimal string.
"""


INPUT = (
        tuple(range(256)), # The list 
        '227,169,3,166,246,201,0,47,1,255,2,254,96,3,97,144' # The lengths
)

from functools import reduce

def parse_as_int(input):
    """ Parse the lenghts as a list of ints """
    return list(map(int, input.split(',')))

def parse_as_str(input):
    """ Parse the lenghts as a list of ints """
    return list(map(ord, input.strip())) + [17, 31, 73, 47, 23]

def calculate_hash(lst, lengths, cp=0, ss=0):
    """ Calculate the hash of the list """
    for length in lengths:
        np = cp + length # next position = current position + length
        wp = int(np/len(lst)) * np % len(lst) # wrap around position
        pinch = list(reversed(lst[cp:np] + lst[:wp]))
        lst[cp:np], lst[:wp] = (pinch[:length-wp], pinch[length-wp:])
        cp = (np + ss) % len(lst)
        ss += 1
    return lst, cp, ss

def get_hash(lengths, parser):
    """ Get the Know Hash """
    lengths = parser(lengths)
    sparse_hash = list(range(256))
    cp = ss = 0
    # Iterate 64 times the hash, keeping current_position and skip_step
    for i in range(64):
        sparse_hash, cp, ss = calculate_hash(sparse_hash, lengths, cp, ss)
    # Get the dense hash
    dense_hash = ( reduce(int.__xor__, block) 
            for block in zip(*[iter(sparse_hash)]*16))
    return ''.join(('{:02x}'.format(block) for block in dense_hash))

def hash_and_get_product(orig_list, lengths, parser):
    """ Hash the list, and return the product of fisrt two elements """
    hash_list, _, _ = calculate_hash(list(orig_list), parser(lengths))
    return hash_list[0] * hash_list[1]

def test(truth, check_function, *args):
    for test_input, result in truth:
        try:
            assert(check_function(*test_input, *args) == result)
        except AssertionError:
            print("Error trying to assert {}({}) == {}".format(
                    check_function.__name__, test_input, result))

if __name__ == "__main__":
    # Test for PART 1
    GROUND_TRUTH = (
            (((0, 1, 2, 3, 4), '3,4,1,5'), 12),
    )
    test(GROUND_TRUTH, hash_and_get_product, parse_as_int)
    # Test for PART 2
    GROUND_TRUTH = (
            (('',), 'a2582a3a0e66e6e86e3812dcb672a272'),
            (('AoC 2017',), '33efeb34ea91902bb2f59c9920caa6cd'),
            (('1,2,3',), '3efbe78a8d82f29979031a4aa0b16a9d'),
            (('1,2,4',), '63960835bcdc130f0b66d7ff4f6a5a8e'),
    )
    test(GROUND_TRUTH, get_hash, parse_as_str)
    # RUN
    print('PART 1 result: {}'.format(hash_and_get_product(*INPUT, parse_as_int)))
    print('PART 2 result: {}'.format(get_hash(INPUT[1], parse_as_str)))
