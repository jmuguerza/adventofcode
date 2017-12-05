#/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 PART 1
 Count the number of instructions executed before leaving the 
 program. Each instruction indicates the number of lines that
 are jumped. Each time an instruction is executed, its jump value
 is incremented by 1.
 PART 2
 Idem, but decrease by 1 if instuction jump is 3 or greater.
"""

FILENAME = 'day5.txt'

import itertools


class Program(object):
    def __init__(self, program):
        self._program = program

    def __next__(self):
        self._last_executed = self._pointer
        try:
            self._pointer += self._program[self._pointer]
            self._life += 1
            return self._last_executed
        except IndexError:
            raise StopIteration

    @property
    def life(self):
        return self._life

    @property
    def last(self):
        return self._last_executed

    def __iter__(self):
        self._pointer = 0
        self._life = 0
        self._last_executed = None
        return self

    def __getitem__(self, key):
        return self._program[key]

    def __setitem__(self, key, value):
        self._program[key] = value
        
def add_one(program):
    """ Add one to last executed instruction """
    program[program.last] += 1

def add_sub_one(program):
    """ Substract from last executed instruction if bigger than 3, else add one """
    program[program.last] += -1 if program[program.last] >= 3 else 1

def get_exit_step(program, alter_func):
    """ Get the number of steps before exiting """
    for last_executed in program:
        alter_func(program)
    return program.life

def check_program_file(filename, function, *args):
    """ Iterate over program file """
    with open(filename) as f:
        program = Program(list(map(int,f.read().rstrip().split('\n'))))
    return function(program, *args)

def test(truth, check_function, *args):
    for test_input, result in truth:
        try:
            assert(check_function(test_input, *args) == result)
        except AssertionError:
            print("Error trying to assert {}({}) == {}".format(
                    check_function.__name__, test_input, result))

if __name__ == "__main__":
    # Test for PART 1
    GROUND_TRUTH = (
            (Program([0, 3, 0, 1, -3]), 5),
    )
    test(GROUND_TRUTH, get_exit_step, add_one)
    # Test for PART 2
    GROUND_TRUTH = (
            (Program([0, 3, 0, 1, -3]), 10),
    )
    test(GROUND_TRUTH, get_exit_step, add_sub_one)
    # RUN
    print('PART 1 result: {}'.format(check_program_file(FILENAME, get_exit_step, add_one)))
    print('PART 2 result: {}'.format(check_program_file(FILENAME, get_exit_step, add_sub_one)))
