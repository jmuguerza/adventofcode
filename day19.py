#/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 PART 1
 The input is a routing diagram. It must follow the lines
 straight, and change course if it is the only option. The
 letters are there to keep track. Which letters are seen 
 when the packets travels?
 PART 2
 Get the number of steps.
"""

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
DOWN = (1,0)
UP = (-1, 0)
RIGHT = (0, 1)
LEFT = (0, -1)

class Diagram(object):
    def __init__(self, diagram):
        self.diagram = tuple(diagram)
        self.word = ""
        self.position = (0, self.diagram[0].index('|'))
        self.dir = DOWN # Start going down
        self.steps = 1

    def route(self):
        """ Route the packet till the end """
        while self.step():
            # Add letter if we are in letter
            curr_char = self.at(self.position)
            if curr_char in LETTERS:
                self.word += curr_char

    def step(self):
        """ Take one step, and return True if we can keep going """
        # Check if next position is valid
        next_position = tuple( self.position[i] + self.dir[i] for i in range(2) )
        next_char = self.at(next_position)
        curr_char = self.at(self.position)
        # If '+', we may need to change direction
        if curr_char == '+':
            if ((self.dir in {UP, DOWN} and next_char in {' ', '-'}) or
                    (self.dir in {LEFT, RIGHT} and next_char in {' ', '|'})):
                # Update dir and next position
                self.change_dir()
                next_position = tuple( self.position[i] + self.dir[i] for i in range(2) )
            self.position = next_position
        # If empty, then it is the end
        elif next_char == ' ':
            return False
        # Else, continue
        else:
            self.position = next_position
        self.steps += 1
        return True

    def change_dir(self):
        """ Change direction, since going straight is not an option """
        if self.dir in {LEFT, RIGHT}:
            if self.at((self.position[0] - 1, self.position[1])) not in {' ', '-'}:
                self.dir = (-1, 0)
            elif self.at((self.position[0] + 1, self.position[1])) not in {' ', '-'}:
                self.dir = (1, 0)
        else:
            if self.at((self.position[0], self.position[1] - 1)) not in {' ', '|'}:
                self.dir = (0, -1)
            elif self.at((self.position[0], self.position[1] + 1)) not in {' ', '|'}:
                self.dir = (0, 1)

    def at(self, position):
        """ Get the value at position """
        try:
            ret = self.diagram[position[0]][position[1]]
        except IndexError:
            ret = ' '
        return ret


def load_and_run(filename, func):
    """ Load the file and run the function """
    with open(filename) as f:
        lines = f.read().splitlines()
    return func(lines)

def get_word(diagram):
    """ Route the packet through diagram, and get the word formed by letters """
    diag = Diagram(diagram)
    diag.route()
    return diag.word

def get_steps(diagram):
    """ Route the packet through diagram, and get the number of steps """
    diag = Diagram(diagram)
    diag.route()
    return diag.steps

def test(truth, check_function, *args):
    for test_input, result in truth:
        try:
            assert(check_function(test_input, *args) == result)
        except AssertionError:
            print("Error trying to assert {}({}) == {}".format(
                    check_function.__name__, test_input, result))

if __name__ == "__main__":
    # Test for PART 1
    GROUND_TRUTH = (('day19_test.txt', "ABCDEF"),)
    test(GROUND_TRUTH, load_and_run, get_word)
    # Test for PART 2
    GROUND_TRUTH = (('day19_test.txt', 38),)
    test(GROUND_TRUTH, load_and_run, get_steps)
    # RUN
    print('PART 1 result: {}'.format(load_and_run('day19.txt', get_word)))
    print('PART 2 result: {}'.format(load_and_run('day19.txt', get_steps)))
