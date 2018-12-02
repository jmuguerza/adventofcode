#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Solutions to the AdventOfCode2018 by Joaquin Muguerza
"""

import re
import argparse
import contextlib
from io import StringIO
from pathlib import Path
from abc import ABC, abstractmethod


@contextlib.contextmanager
def open_file_or_string(string):
    if Path(string).is_file():
        f = open(string, 'r')
        yield f
        f.close()
    else:
        yield StringIO(string)


class Puzzle(ABC):
    def __init__(self, *args, **kwargs):
        pass

    def run(self, part_one=True, part_two=True, *args, **kwargs):
        self.parse_input()
        result_part_one = self.part_one() if part_one else None
        result_part_two = self.part_two() if part_two else None
        return (result_part_one, result_part_two)

    @abstractmethod
    def parse_input(self):
        ...

    @classmethod
    def add_subparser(cls, subparsers):
        parser = subparsers.add_parser(
                str(cls.DAY),
                help="Execute day {} puzzle".format(cls.DAY))
        parser.add_argument(
                'input_file', type=str,
                help="Input string or path to file containing input"
        )

    @property
    @abstractmethod
    def DAY(self):
        raise NotImplementedError


class Puzzle1(Puzzle):
    DAY = 1

    def __init__(self, *args, **kwargs):
        self.input_file = kwargs['input_file']

    def parse_input(self):
        with open_file_or_string(self.input_file) as f:
            self.changes = list(map(int, f.readlines()))

    def part_one(self):
        """ First part of the puzzle: return the sum of all numbers in file """
        total = sum(self.changes)
        return total

    def part_two(self):
        """ Get the first number reached twice """
        total = 0
        reached = {0}
        twice_found = False
        while not twice_found:
            for change in self.changes:
                total += change
                if total in reached:
                    twice_found = True
                    break
                reached.add(total)
        return total


def get_puzzle_classes():
    """ Return an iterator of all Puzzle classes """
    return (
            cls for class_name, cls in globals().items()
            if re.match('^Puzzle[0-9]+$', class_name)
    )

def get_puzzle_class(puzzle_number):
    """ Return the class of one puzzle """
    return globals()['Puzzle{}'.format(puzzle_number)]

def get_parser():
    """ Construct a parser with all submodules """
    parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    subparsers = parser.add_subparsers(
            title='Puzzles',
            dest='puzzle_number',
            metavar='puzzle_number',
            description='Valid puzzles',
    )
    subparsers.required = True

    # Add subparser of each puzzle class
    for puzzle_class in get_puzzle_classes():
        puzzle_class.add_subparser(subparsers)

    return parser

if __name__ == '__main__':
    args = get_parser().parse_args()
    puzzle = get_puzzle_class(args.puzzle_number)(**vars(args))
    results = puzzle.run()
    print("Part one: {}".format(results[0]))
    print("Part two: {}".format(results[1]))
