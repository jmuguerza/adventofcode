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
"""


INPUT = (
        tuple(range(256)), # The list 
        (227,169,3,166,246,201,0,47,1,255,2,254,96,3,97,144) # The lengths
)

def calculate_hash(lst, lengths):
    """ Calculate the hash of the list """
    cp = ss = 0 # current position = skip size = 0
    for length in lengths:
        np = cp + length # next position = current position + length
        wp = int(np/len(lst)) * np % len(lst) # wrap around position
        pinch = list(reversed(lst[cp:np] + lst[:wp]))
        lst[cp:np], lst[:wp] = (pinch[:length-wp], pinch[length-wp:])
        cp = (np + ss) % len(lst)
        ss += 1
    return lst

def hash_and_get_product(orig_list, lengths):
    """ Hash the list, and return the product of fisrt two elements """
    hash_list = calculate_hash(list(orig_list), lengths)
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
            (((0, 1, 2, 3, 4), (3, 4, 1, 5)), 12),
    )
    test(GROUND_TRUTH, hash_and_get_product)
    # RUN
    print('PART 1 result: {}'.format(hash_and_get_product(*INPUT)))
