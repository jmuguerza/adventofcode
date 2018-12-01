#/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 PART 1
 There is a virus on a infected grid. Each node is either clean or infected.
 There is only one virus that is moving, and infecting. It keeps track of
 the direction its facing. It works in bursts: wakes up, works, sleeps.
 - If current node is infected, turns to its right, else turns left.
 - If current node is clean, it becomes infected, else becomes cleaned.
 - Moves forward one node.
 Virus begins in center of given map, facing up. After 10000 bursts of
 activiy, how many have caused a node to get infetcted?
 PART 2
 Now, instead of cleaning or infecting, clean becomes, weakened, then infected;
 infected becomes flagged then clean.
 Now, if clean, turn left, if weakened does not turn, infected, right. If flagged
 reverses.
"""

UP    = (-1,  0)
DOWN  = ( 1,  0)
LEFT  = ( 0, -1)
RIGHT = ( 0,  1)

CLEAN    = '.'
INFECTED = '#'
WEAKENED = 'W'
FLAGGED  = 'F'

import cmath
from collections import defaultdict

class Virus(object):
    def __init__(self, grid):
        self.pos = (0, 0)
        self.dir = UP
        self.grid = grid
        self.infective = 0

    def rotate(self, clockwise=True):
        """ rotate clockwise or anticlockwise """
        is_infected = self.grid[self.pos] == INFECTED
        rotation = complex(-1j) if is_infected else complex(1j)
        new_dir = complex(*self.dir) * rotation
        self.dir = int(new_dir.real), int(new_dir.imag)

    def advance(self):
        """ advance one step """
        self.pos = tuple( self.pos[i] + self.dir[i] for i in range(2) )

    def infect(self):
        """ infect or clean current position """
        is_infected = self.grid[self.pos] == INFECTED
        self.grid[self.pos] = CLEAN if is_infected else INFECTED
        self.infective += 1 if not is_infected else 0

    def burst(self):
        """ make a burst, return True if was infective """
        self.rotate()
        self.infect()
        self.advance()

class NewVirus(Virus):
    def rotate(self, clockwise=True):
        """ reverse, continue or rotate clockwise or anticlockwise """
        rotation = (
                complex(1) if self.grid[self.pos] == WEAKENED else
                complex(1j) if self.grid[self.pos] == CLEAN else
                complex(-1j) if self.grid[self.pos] == INFECTED else
                complex(-1))
        new_dir = complex(*self.dir) * rotation
        self.dir = int(new_dir.real), int(new_dir.imag)

    def infect(self):
        """ change infection status """
        self.infective += 1 if self.grid[self.pos] == WEAKENED else 0
        self.grid[self.pos] = (
                WEAKENED if self.grid[self.pos] == CLEAN else
                INFECTED if self.grid[self.pos] == WEAKENED else
                FLAGGED if self.grid[self.pos] == INFECTED
                else CLEAN )

def get_grid(lines):
    """ initialize grid from input file """
    offset = int((len(lines)-1)/2)
    grid = defaultdict(lambda: CLEAN, {
            (i-offset, j-offset): lines[i][j]
            for i in range(len(lines))
            for j in range(len(lines))
    })
    return grid

def get_infecting_bursts(lines, n_iterations, virus_class):
    """ get the number of infecting bursts after n iterations """
    grid = get_grid(lines)
    n_infective = 0
    virus = virus_class(grid)
    for i in range(n_iterations):
        virus.burst()
    return virus.infective

def load_and_run(filename, func, *args):
    """ Load the file and run the function """
    with open(filename) as f:
        lines = f.read().splitlines()
    return func(lines, *args)

def test(truth, check_function, *args):
    for test_input, expected_result in truth:
        try:
            result = check_function(test_input, *args)
            assert(result == expected_result)
        except AssertionError:
            print("Error trying to assert {}({}) = {} == {} ".format(
                    check_function.__name__, test_input, result, expected_result))

if __name__ == "__main__":
    # Test for PART 1
    GROUND_TRUTH = (('day22_test.txt', 5587),)
    test(GROUND_TRUTH, load_and_run, get_infecting_bursts, 10000, Virus)
    # Test for PART 2
    GROUND_TRUTH = (('day22_test.txt', 2511944),)
    test(GROUND_TRUTH, load_and_run, get_infecting_bursts, 10000000, NewVirus)
    # RUN
    print('PART 1 result: {}'.format(load_and_run('day22.txt', get_infecting_bursts, 10000, Virus)))
    print('PART 2 result: {}'.format(load_and_run('day22.txt', get_infecting_bursts, 10000000, NewVirus)))
