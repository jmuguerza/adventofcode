#/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 PART 1
 Get the shortest distance from the start of a center grid to
 the last point.
 PART 2
 Get the furthest point ever.
"""

from collections import defaultdict

DIRS = {
        'n' : ( 0, 2),
        'ne': ( 1, 1),
        'nw': (-1, 1),
        's' : ( 0,-2),
        'se': ( 1,-1),
        'sw': (-1,-1)
}

def load_and_run(filename, func):
    """ Load the file and run the function """
    with open(filename) as f:
        return func(f.read().rstrip())

def subs_abs(x, y):
    """ Decrease absolute value of X by Y, return X """
    return abs(x) - abs(y) if x > 0 else abs(y) - abs(x)

def get_distance(orig_pos):
    """ Get the min distance after following steps """
    diag = abs(min(orig_pos, key=abs))
    return int(0.5* (abs(orig_pos[1]) - diag) + abs(orig_pos[0]))

def avance(position, step):
    """ Avance one step from position """
    return list(sum(pos) for pos in zip(position, DIRS[step]))

def final_distance(steps):
    """ Get distance from steps """
    position = (0, 0)
    for step in steps.split(','):
        position = avance(position, step)
    return get_distance(position)

def furthest_distance(steps):
    """ Get furthest distance from steps """
    position = (0, 0)
    distance = 0
    for step in steps.split(','):
        position = avance(position, step)
        distance = max(distance, get_distance(position))
    return distance

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
            ('ne,ne,ne', 3),
            ('ne,ne,sw,sw', 0),
            ('ne,ne,s,s', 2),
            ('se,sw,se,sw,sw', 3),
    )
    test(GROUND_TRUTH, final_distance)
    # Test for PART 2
    GROUND_TRUTH = (
            ('ne,ne,ne', 3),
            ('ne,ne,sw,sw', 2),
            ('ne,ne,s,s', 2),
            ('se,sw,se,sw,sw', 3),
    )
    test(GROUND_TRUTH, furthest_distance)
    # RUN
    print('PART 1 result: {}'.format(load_and_run('day11.txt', final_distance)))
    print('PART 2 result: {}'.format(load_and_run('day11.txt', furthest_distance)))
