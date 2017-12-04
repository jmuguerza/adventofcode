#/usr/bin/env python3
# -*- coding: utf-8 -*-

# PART 1
# A new kind of memory is used to store info in an infinite
# two dimentional grid. Each square of the grid is allocated
# in an spiral pattern starting at a location marked 1, and
# then counting up while spiraling outward. Data is carried
# always from the square 1, using the minimum distance.

INPUT = 312051


def manhattan_distance(position):
    # TODO 


def test(truth, distance_calculator):
    for position, result in truth:
        try:
            assert(distance_calculator(position) == result)
        except AssertionError:
            print("Error trying to assert {}('{}') == {}".format(
                    distance_calculator.__name__, position, distance))

if __name__ == "__main__":
    # Test for PART 1
    GROUND_TRUTH = (
            (1, 0),
            (12, 3),
            (23, 20),
            (1024, 31),
            )
    test(GROUND_TRUTH, manhattan_distance)
    # RUN
    print('PART 1 result: {}'.format(manhattan_distance(INPUT)))
