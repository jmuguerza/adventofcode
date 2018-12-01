"""Solutions to the AdventOfCode2018 by Joaquin Muguerza
"""

import re
import argparse
from abc import ABC, abstractmethod


class Puzzle(ABC):

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def run(self, *args, **kwargs):
        ...

    @staticmethod
    def add_subparser(subparsers):
        pass


class Puzzle1(Puzzle):

    def __init__(self, *args, **kwargs):
        self.input_file = kwargs['input_file']

    def run(self, *args, **kwargs):
        with self.input_file as f:
            self.changes = list(map(int, f.readlines()))
        self.part_one()
        self.part_two()

    def part_one(self):
        """ First part of the puzzle: return the sum of all numbers in file """
        total = sum(self.changes)
        print("Part one:{}".format(total))

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
        print("Part two:{}".format(total))

    @staticmethod
    def add_subparser(subparsers):
        parser = subparsers.add_parser('1', help="Execute day 1 puzzle")
        parser.add_argument(
                'input_file', type=argparse.FileType('r'),
                help="File containing the puzzle input"
        )

def get_puzzle_classes():
    """ Return an iterator of all Puzzle classes """
    return (
            cls for class_name, cls in globals().items()
            if re.match('Puzzle[0-9]+', class_name)
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
    puzzle.run()
