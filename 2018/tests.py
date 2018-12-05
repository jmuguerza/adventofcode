#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Test-suite for puzzle solvers"""

import re
import argparse
from abc import ABC

from solvers import *

class TestPuzzle(ABC):
    def __init__(self, *args, **kwargs):
        super()
        self.test_class = globals()['Puzzle{}'.format(self.DAY)]
        self.test_cases = []
        self.load_test_cases()

    @abstractmethod
    def load_test_cases(self):
        pass

    def run(self, *args, **kwargs):
        for test_case in self.test_cases:
            print("Testing Puzzle {} with input '{}'".format(
                self.DAY, test_case['input'].encode('unicode-escape').decode()))
            # Instantiate a class
            puzzle = self.test_class(test_case['input'])
            # Run puzzle
            results = puzzle.run(part_one='result_part_one' in test_case,
                    part_two='result_part_two' in test_case)
            # Compare results
            if 'result_part_one' in test_case:
                print("\tPart one: got result: {}, was expecting: {} ... {}".format(
                    results[0], test_case['result_part_one'],
                    'PASS' if results[0] == test_case['result_part_one'] else 'FAIL'))
            if 'result_part_two' in test_case:
                print("\tPart two: got result: {}, was expecting: {} ... {}".format(
                    results[1], test_case['result_part_two'],
                    'PASS' if results[1] == test_case['result_part_two'] else 'FAIL'))

    def add_test_case(self, input_string,
            result_part_one=None,
            result_part_two=None):
        test_case = dict(input=input_string)
        if result_part_one is not None:
            test_case.update(dict(result_part_one=result_part_one))
        if result_part_two is not None:
            test_case.update(dict(result_part_two=result_part_two))
        self.test_cases.append(test_case)

    @property
    @abstractmethod
    def DAY(self):
        raise NotImplementedError

class TestPuzzle1(TestPuzzle):
    DAY = 1

    def load_test_cases(self):
        self.add_test_case('+1\n+1\n+1', result_part_one=3)
        self.add_test_case('+1\n+1\n-2', result_part_one=0)
        self.add_test_case('-1\n-2\n-3', result_part_one=-6)
        self.add_test_case('+1\n-1', result_part_two=0)
        self.add_test_case('+3\n+3\n+4\n-2\n-4', result_part_two=10)
        self.add_test_case('-6\n+3\n+8\n+5\n-6', result_part_two=5)
        self.add_test_case('+7\n+7\n-2\n-7\n-4', result_part_two=14)

class TestPuzzle2(TestPuzzle):
    DAY = 2

    def load_test_cases(self):
        test_input = (
                "abcdef", "bababc", "abbcde", "abcccd",
                "aabcdd", "abcdee", "ababab")
        self.add_test_case('\n'.join(test_input), result_part_one=12)
        test_input = (
                "abcde", "fghij", "klmno", "pqrst", "fguij",
                "axcye", "wvxyz")
        self.add_test_case('\n'.join(test_input), result_part_two='fgij')

class TestPuzzle3(TestPuzzle):
    DAY = 3

    def load_test_cases(self):
        test_input = (
                "#1 @ 1,3: 4x4", "#2 @ 3,1: 4x4", "#3 @ 5,5: 2x2")
        self.add_test_case('\n'.join(test_input),
                result_part_one=4, result_part_two=3)


def get_parser():
    """ Construct a parser """
    parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
            'puzzle_number', type=int,
            choices=list(puzzle.DAY for puzzle in get_puzzle_classes()),
            help='Puzzle number to test', metavar='puzzle_number')

    return parser

def get_test_class(puzzle_number):
    """ Return the class of one puzzle """
    return globals()['TestPuzzle{}'.format(puzzle_number)]


if __name__ == '__main__':
    args = get_parser().parse_args()
    tester = get_test_class(args.puzzle_number)()
    tester.run()
