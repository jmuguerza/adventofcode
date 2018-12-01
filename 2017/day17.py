#/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 PART 1
 There's a spinlock with the following algorithm:
 * starts with a circular buffer filled with zeros.
 * steps forward some number, and inserts a 1 after the number
   it stopped on. The inserted value becomes the current position.
 * Idem, but inserts a 2. Rinse and repeat. 
 The algorithm is repeated 2017 times. What's the value after the 
 last inserted 2017 ?
 PART 2
 Get the value after 0, after the 50000000th insertion
"""

INPUT = 343
N_INSERTIONS_1 = 2017
N_INSERTIONS_2 = 50000000


def get_one_after(steps):
    """ Get what's the number after the last insertion """
    vector = [0]
    inserting_pos = 0
    for inserting in range(1, N_INSERTIONS_1+1):
        initial_pos = inserting_pos + 1 
        inserting_pos = (initial_pos + steps) % inserting
        vector = vector[:inserting_pos + 1]  + [inserting] + vector[inserting_pos + 1:]
    return vector[inserting_pos + 2]

def get_after_zero(steps):
    """ Get what's the number after 0 after the last insertion """
    vector = [0]
    inserting_pos = 0
    after_zero = -1
    for inserting in range(1, N_INSERTIONS_2+1):
        initial_pos = inserting_pos + 1 
        inserting_pos = (initial_pos + steps) % inserting
        if not inserting_pos:
            after_zero = inserting
    return after_zero

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
            (3, 638),
    )
    test(GROUND_TRUTH, get_one_after)
    # RUN
    print('PART 1 result: {}'.format(get_one_after(INPUT)))
    print('PART 2 result: {}'.format(get_after_zero(INPUT)))
