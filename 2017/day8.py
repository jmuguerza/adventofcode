#/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 PART 1
 We receive a set of instructions. Each instruction consists of 
 several parts: register to modify, whether to increase or decrease,
 and the condition. If the condition fails, skip the instruction.
 What's the largest value of any register by the end? 
 PART 2
 Get the highest value ever.
"""

import re
from collections import defaultdict

REGEX = r'([a-zA-Z]+) (inc|dec) ([-0-9]+) if (.*)'


def execute(memory, name, action, value, condition):
    """ Executes a line of the program. Returns new value """
    value = int(value) if action == 'inc' else -int(value)
    dest, comp, comp_value = condition.split()
    comp = (
            memory[dest].__eq__ if comp == '==' else
            memory[dest].__ne__ if comp == '!=' else
            memory[dest].__gt__ if comp == '>' else
            memory[dest].__ge__ if comp == '>=' else
            memory[dest].__lt__ if comp == '<' else
            memory[dest].__le__ if comp == '<=' else
            None
            )
    memory[name] += value if comp(int(comp_value)) else 0
    return memory[name]

def load_and_run(filename, func):
    """ Load the file and run the function """
    with open(filename) as f:
        program = re.findall(REGEX, f.read())
    return func(program)

def get_biggest(program):
    """ Return biggest register in the memory """
    memory = defaultdict(int)
    for name, action, value, condition in program:
        execute(memory, name, action, value, condition)
    return max(memory.values())

def get_biggest_ever(program):
    """ Return biggest ever register in the memory """
    memory = defaultdict(int)
    biggest = 0
    for name, action, value, condition in program:
        biggest = max(biggest, execute(memory, name, action, value, condition))
    return biggest

def test(truth, check_function, *args):
    for test_input, result in truth:
        try:
            assert(check_function(test_input, *args) == result)
        except AssertionError:
            print("Error trying to assert {}({}) == {}".format(
                    check_function.__name__, test_input, result))

if __name__ == "__main__":
    # Test for PART 1
    GROUND_TRUTH = (('day8_test.txt', 1),)
    test(GROUND_TRUTH, load_and_run, get_biggest)
    # Test for PART 2
    GROUND_TRUTH = (('day8_test.txt', 10),)
    test(GROUND_TRUTH, load_and_run, get_biggest_ever)
    # RUN
    print('PART 1 result: {}'.format(load_and_run('day8.txt', get_biggest)))
    print('PART 2 result: {}'.format(load_and_run('day8.txt', get_biggest_ever)))
