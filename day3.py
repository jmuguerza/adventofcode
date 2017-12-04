#/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 PART 1
 A new kind of memory is used to store info in an infinite
 two dimentional grid. Each square of the grid is allocated
 in an spiral pattern starting at a location marked 1, and
 then counting up while spiraling outward. Data is carried
 always from the square 1, using the minimum distance.
"""

INPUT = 312051


import math

def get_side_length(position):
    """ Get the side length of the square where
        the position is found.
        
        Each square goes up to L^2, where L = 2d+1,
        L is the side length, and d is the distance
        to the center."""
    side = math.ceil(math.sqrt(position))
    return side if side % 2 else side + 1

def manhattan_distance(position):
    """ Get the manhattan distance for position """
    # Get the square side length
    side = get_side_length(position)

    # Get the shortest distance to a side center
    d_to_side_center = min([
        abs(position - (side**2 - 0.5 * (side - 1))),
        abs(position - (side**2 - 1.5 * (side - 1))),
        abs(position - (side**2 - 2.5 * (side - 1))),
        abs(position - (side**2 - 3.5 * (side - 1))),
        ])

    # The manhattan distance is equal to the shortest
    # distance to the side center plus the distance 
    # from it, to the square center
    return int(d_to_side_center + 0.5 * (side - 1))


def test(truth, distance_calculator):
    for position, result in truth:
        try:
            assert(distance_calculator(position) == result)
        except AssertionError:
            print("Error trying to assert {}('{}') == {}".format(
                    distance_calculator.__name__, position, result))

if __name__ == "__main__":
    # Test for PART 1
    GROUND_TRUTH = (
            (1, 0),
            (12, 3),
            (23, 2),
            (1024, 31),
            )
    test(GROUND_TRUTH, manhattan_distance)
    # RUN
    print('PART 1 result: {}'.format(manhattan_distance(INPUT)))
