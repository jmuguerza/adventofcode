#/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 PART 1
 Two generators produce codes. A judge counts the number 
 of times the lowest 16 bits of these codes are equal, in 
 40 million pairs. Each code is generated from previous 
 generated code, multiplying to factor, and then getting 
 the remainder of the division by a number.
 PART 2
 Idem, but a code generator only returns the codes that
 are multiples of a certain number.
"""

from functools import partial

INPUT = (783, 325)
A_FACTOR = 16807
B_FACTOR = 48271
DIVISOR = 2147483647
N_TIMES_1 = int(4e7)
N_TIMES_2 = int(5e6)
MULTIP_A = 4
MULTIP_B = 8

def get_codes(prev_code, factor, divisor=DIVISOR, multip=1):
    """ Generate the codes from previous codes """
    while True:
        prev_code = (prev_code * factor) % divisor
        if prev_code % multip == 0:
            return prev_code

def get_equal_16bits(first_n, n_times=N_TIMES_1):
    """ Get the number of pairs with matching lowest 16 bits """
    codes = first_n
    equal = 0
    for i in range(n_times):
        codes = list(get_codes(prev, factor) for prev, factor
                in zip(codes, (A_FACTOR, B_FACTOR)))
        if (codes[0] & 0xFFFF == codes[1] & 0xFFFF):
            equal += 1
    return equal

def get_equal_16bits_2(first_n, n_times=N_TIMES_2):
    """ Get the number of pairs with matching lowest 16 bits """
    codes = first_n
    equal = 0
    gen_a = partial(get_codes, multip=MULTIP_A)
    gen_b = partial(get_codes, multip=MULTIP_B)
    for i in range(n_times):
        codes = list(gen(prev, factor) for prev, factor, gen
                in zip(codes, (A_FACTOR, B_FACTOR), (gen_a, gen_b)))
        if (codes[0] & 0xFFFF == codes[1] & 0xFFFF):
            equal += 1
    return equal

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
            ((65, 8921), 588),
    )
    test(GROUND_TRUTH, get_equal_16bits)
    # Test for PART 2
    GROUND_TRUTH = (
            ((65, 8921), 309),
    )
    test(GROUND_TRUTH, get_equal_16bits_2)
    # RUN
    print('PART 1 result: {}'.format(get_equal_16bits(INPUT)))
    print('PART 2 result: {}'.format(get_equal_16bits_2(INPUT)))
