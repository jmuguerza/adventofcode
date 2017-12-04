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
import itertools
from collections import defaultdict

# Store already calculated sums to avoid recalculation
calculated_sums = defaultdict(int)

def get_side_length(position):
    """ Get the side length of the square where
        the position is found.
        
        Each square goes up to L^2, where L = 2d+1,
        L is the side length, and d is the distance
        to the center."""
    side = math.ceil(math.sqrt(position))
    return side if side % 2 else side + 1

def is_corner(position):
    """ True if position is in a corner of a square """
    if position == 1:
        return False
    side = get_side_length(position)
    corners = {
            int(side**2),
            int(side**2 - 1 * (side - 1)),
            int(side**2 - 2 * (side - 1)),
            int(side**2 - 3 * (side - 1)),
    }
    return position in corners

def is_not_corner(position):
    """ True if position is not a corner of a square """
    if position == 1:
        return False
    return not is_corner(position)

def get_distance_to_inner(position):
    """ Get the distance to a position in the inner square """
    # Difference between positions square and inners square depends on side
    # For RIGHT side, is D=4*(L-1)+1, where L is the size of inner square
    # For TOP side is D+2, LEFT D+4, BOTTOM D+6
    L = get_side_length(position)
    inner_L = L - 2
    if position > (L**2  - (L -1)):
        return 4 * (inner_L - 1) + 7
    if position > (L**2  - 2 * (L -1)):
        return 4 * (inner_L - 1) + 5
    if position > (L**2  - 3 * (L -1)):
        return 4 * (inner_L - 1) + 3
    else:
        return 4 * (inner_L - 1) + 1

def square_smallest(length):
    """ Get the smallest number of a square """
    if length == 1:
        return 1
    return (length - 2)**2 + 1

def get_adjacent(position):
    """ Get smaller adjacent positions for a position """
    if position == 1:
        return []
    # Previous position is always adjacent
    adj = {position - 1}
    # Get adjacent positions in inner square
    L = get_side_length(position)
    D = get_distance_to_inner(position)
    if is_corner(position):
        # 1. the one diagonally in
        adj.add(position - D - 1)
        # 2. if last corner, then the first element of square
        if position == L ** 2:
            adj.add(position - 4 * L + 5)
    else:
        # If it's the first of the square, then just add smallest of inner square
        if position == square_smallest(L):
            adj.add(square_smallest(L - 2))
        else:
            # 1. the one right next to it
            if is_not_corner(position):
                adj.add(position - D)
            # 2. the one diagonally inner back
            #    (smaller + 1 has a different expression)
            if is_not_corner(position - 1):
                if position == square_smallest(L) + 1:
                    adj.add((L - 2)**2)
                else:
                    adj.add(position - D - 1)
            # 3. the one diagonally inner front
            if is_not_corner(position + 1):
                adj.add(position - D + 1)
            # 4. if the next is the last of the square, then
            #    the first of the square is adjacent
            if position + 1 == L ** 2:
                adj.add(square_smallest(L))
            # 5. If previous is in a corner, then position - 2 is adjacent
            if is_corner(position - 1):
                adj.add(position - 2)
    yield from adj

def adjacent_sum(position):
    """ Get the sum of all lesser adjacent positions """
    if not calculated_sums[position]:
        for adj_position in get_adjacent(position):
            calculated_sums[position] += adjacent_sum(adj_position)
    return calculated_sums[position]

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
    # Store value for first position
    calculated_sums[1] = 1
    # Test for PART 1
    GROUND_TRUTH = (
            (1, 0),
            (12, 3),
            (23, 2),
            (1024, 31),
            )
    test(GROUND_TRUTH, manhattan_distance)
    # Test for PART 2
    GROUND_TRUTH = (
            (1, 1),
            (2, 1),
            (3, 2),
            (4, 4),
            (5, 5),
            (6, 10),
            (7, 11),
            (8, 23),
            (9, 25),
            (10, 26),
            (11, 54),
            (12, 57),
            (13, 59),
            (14, 122),
            (15, 133),
            (16, 142),
            (17, 147),
            (18, 304),
            (19, 330),
            (20, 351),
            (21, 362),
            (22, 747),
            (23, 806),
    )
    test(GROUND_TRUTH, adjacent_sum)
    # RUN
    print('PART 1 result: {}'.format(manhattan_distance(INPUT)))
    for i in itertools.count(start=1):
        if adjacent_sum(i) > INPUT:
            print('PART 2 result: {}'.format(adjacent_sum(i)))
            break
