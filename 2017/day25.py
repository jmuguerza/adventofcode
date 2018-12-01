#/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 PART 1
 We have to build a Turing machine from blueprints. The blueprints
 contain:
 - a tape, which contains 0 repeated infinitely to the left and the right.
 - a cursor, which can move either left or right along the type, and that
   can read and write to the current position.
 - a set if states, containing rules about what to do based on current value.
 Each slot on the tape can have only two values, 0 or 1. Based on this value,
 the state says what to write, whether to move to left or right, and which 
 state to use next.
 Whats the checksum after N steps (provided in blueprints) ?
"""

import re
import sys
from collections import defaultdict

class State:
    START_STATE = re.compile(r'^In state ([A-Z]):')
    START_CONDITION = re.compile(r'If the current value is ([01]):')
    WRITE_VALUE = re.compile(r'- Write the value ([01])')
    MOVE = re.compile(r'- Move one slot to the (right|left)')
    NEXT_STATE = re.compile(r'- Continue with state ([A-Z])')

    def __init__(self, name):
        self.name = name
        self.current_value = {}

    def __hash__(self):
        return self.name.__hash__()

    def __eq__(self, other):
        return self.name == other

    def __getitem__(self, index):
        return self.current_value[index]

    def add_condition(self, current_value, lines):
        """ Add condition for current value """
        self.current_value[int(current_value)] = {}
        for line in lines:
            write = self.WRITE_VALUE.search(line)
            move = self.MOVE.search(line)
            next_state = self.NEXT_STATE.search(line)
            if write:
                self.current_value[int(current_value)].update(
                        write=int(write.group(1)))
            elif move:
                self.current_value[int(current_value)].update(
                        move=(-1 if move.group(1) == 'left' else 1))
            elif next_state:
                self.current_value[int(current_value)].update(
                        next=next_state.group(1))
            if len(self.current_value[int(current_value)]) == 3:
                return

    @classmethod
    def build_states(cls, lines):
        """ Build a state from lines """
        state = None
        for line in lines:
            start_state = cls.START_STATE.search(line)
            start_condition = cls.START_CONDITION.search(line) 
            if start_state:
                if state:
                    yield state
                state = cls(start_state.group(1))
            elif start_condition:
                state.add_condition(start_condition.group(1), lines)
        yield state

class TuringMachine:
    FIRST_STATE = re.compile(r'Begin in state ([A-Z])')
    CHECKSUM = re.compile(r'Perform a diagnostic checksum after (\d+) steps')

    def __init__(self):
        self.pointer = 0
        self.tape = defaultdict(lambda: 0)
        self.states = {}
        self.state = None
        self.steps = 0

    def add_states(self, lines):
        """ Create states from lines """
        for state in State.build_states(lines):
            self.states[state] = state

    def run(self):
        """ Run Turing machine """
        for step in range(self.steps):
            current_value = self.tape[self.pointer]
            self.tape[self.pointer] = self.states[self.state][current_value]['write']
            self.pointer += self.states[self.state][current_value]['move']
            self.state = self.states[self.state][current_value]['next']

    def checksum(self):
        """ Return checksum """
        return sum(self.tape.values())

    @classmethod
    def build_from_lines(cls, lines):
        """ Build a Turing machine from lines """
        turing_machine = cls()

        for line in lines:
            first_state = cls.FIRST_STATE.search(line)
            checksum = cls.CHECKSUM.search(line)
            if first_state:
                turing_machine.state = first_state.group(1)
            elif checksum:
                turing_machine.steps = int(checksum.group(1))
                turing_machine.add_states(lines)
        return turing_machine


def get_checksum(lines):
    """ Build the machine, execute it, and return the checksum """
    turing = TuringMachine.build_from_lines(iter(lines))
    turing.run()
    return turing.checksum()

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
            sys.exit(1)

if __name__ == "__main__":
    # Test for PART 1
    GROUND_TRUTH = (('day25_test.txt', 3),)
    test(GROUND_TRUTH, load_and_run, get_checksum)
    # RUN
    print('PART 1 result: {}'.format(load_and_run('day25.txt', get_checksum)))
