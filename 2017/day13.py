#/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 PART 1
 A firewoll has several layers, with depth:range.
 Each layer has a thickness of exactly 1. In each layer,
 a scanner moves within the range, starting on top, and 
 going to the bottom, one step every ps. You move on a packet,
 transversing one layer every ps, along the top. The severity
 of getting caught is equal to its depth times the range.
 What's the severity for the whole trip?
 PART 2
 Get the smallest delay to cross without being caught
"""


from itertools import count


def iterate_firewall(text):
    """ Iterate over the firewall """
    for line in text.split('\n'):
        yield tuple(map(int, line.split(':')))

def load_and_run(filename, func):
    """ Load the file and run the function """
    with open(filename) as f:
        return func(f.read().rstrip())

def get_severity(firewall_input):
    """ Get the severity after passing through the firewall """
    severity = 0
    for depth, rang in iterate_firewall(firewall_input):
        severity += depth * rang if (depth % (2*rang-2)) == 0 else 0
    return severity

def get_delay_uncaught(firewall_input):
    """ Get the smallest delay to cross the firewall without being caught """
    for delay in count():
        caught = False
        for depth, rang in iterate_firewall(firewall_input):
            if ((depth + delay) % (2*rang-2)) == 0:
                caught = True
                break
        if not caught:
            return delay

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
            ('day13_test.txt', 24),
    )
    test(GROUND_TRUTH, load_and_run, get_severity)
    # Test for PART 2
    GROUND_TRUTH = (
            ('day13_test.txt', 10),
    )
    test(GROUND_TRUTH, load_and_run, get_delay_uncaught)
    # RUN
    print('PART 1 result: {}'.format(load_and_run('day13.txt', get_severity)))
    print('PART 2 result: {}'.format(load_and_run('day13.txt', get_delay_uncaught)))
