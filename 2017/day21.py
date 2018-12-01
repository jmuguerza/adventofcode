#/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 PART 1
 A program generates art, by enhancing images. Each pixel
 consists of '.' (off) and '#' (on), and the program always
 begins with the same pattern (3x3). The algorithm is the 
 following:
 - if the size is even, break each pixel into 2x2, and convert
   each 2x2 square into a 3x3 square, according to the proper
   enhancement rule.
 - if the size is divisible by 3, break the pixels in 3x3 squares,
   and convert each 3x3 square into a 4x4 square, according to the
   appropiate enhancement rule.
 The list of rules is not complete. Sometimes you have to flip, or
 rotate the input pattern to find a match.
 How many pixels are ON after 5 iterations?
 PART 2
 How many pixels stay ON after 18 iterations?
"""

from math import sqrt


BEGIN_BLOCK = '.#./..#/###'

def rotate(block):
    """ rotate a block """
    rows = block.split('/')
    cols = tuple(map(''.join, zip(*rows)))
    return '/'.join(reversed(cols))

def reflect_vertical(block):
    """ reflect vertically a block """
    rows = block.split('/')
    return '/'.join(reversed(rows))

def reflect_horizontal(block):
    """ reflect horizontally a block """
    rows = tuple(''.join(reversed(row)) for row in block.split('/'))
    return '/'.join(rows)

def rotations(input):
    """ Get all possible rotations of rule """
    for i in range(4):
        yield input
        input = rotate(input)

def transform(rule):
    """ Get all possible transformations of rule (rotations and reflections) """
    input, output = rule.split(' => ')
    for rotation in rotations(input):
        yield rotation, output
        yield reflect_vertical(rotation), output
        yield reflect_horizontal(rotation), output
        yield reflect_vertical(reflect_horizontal(rotation)), output

def create_rules(rules_input):
    """ create rules, and return dictionary of enhancements """
    rules = {}
    for rule in rules_input:
        rules.update({ 
                rule_trans: out_trans for rule_trans, out_trans 
                in transform(rule) 
                    })
    return rules

def get_subblocks(block):
    """ get all subblocks of a block """
    rows = block.split('/')
    if len(rows) % 2 == 0:
        subblock_size = 2 
    elif len(rows) % 3 == 0:
        subblock_size = 3
    else:
        raise Exception("Wrong block size")
    for i in range(int(len(rows) / subblock_size)):
        subblock_rows = rows[i*subblock_size:(i+1)*subblock_size]
        for j in range(int(len(subblock_rows[0]) / subblock_size)):
            yield '/'.join(
                    row[j*subblock_size:(j+1)*subblock_size]
                    for row in subblock_rows
            )

def get_block(subblocks):
    """ get the resulting block from all subblocks """
    rows = []
    N = int(sqrt(len(subblocks)))
    subblock_size = len(subblocks[0].split('/')[0])
    for i in range(N):
        for j in range(subblock_size):
            rows.append(''.join(
                    subblock_rows[j] 
                    for subblock in subblocks[i*N:(i+1)*N]
                    for subblock_rows in subblock.split('/')))
    return '/'.join(rows)

def get_on_after_iterations(rules, n_iterations):
    """ Get the number of ON bits after N iterations """
    rules = create_rules(rules)
    block = BEGIN_BLOCK
    for i in range(n_iterations):
        # Divide in subblocks, and enhance
        subblocks = tuple( rules[subblock] for subblock in get_subblocks(block) )
        # Get the whole block
        block = get_block(subblocks)
    return block.count('#')


def load_and_run(filename, func, *args):
    """ Load the file and run the function """
    with open(filename) as f:
        lines = f.read().splitlines()
    return func(lines, *args)

def test(truth, check_function, *args):
    for test_input, result in truth:
        try:
            assert(check_function(test_input, *args) == result)
        except AssertionError:
            print("Error trying to assert {}({}) == {}".format(
                    check_function.__name__, test_input, result))

if __name__ == "__main__":
    # Test for PART 1
    GROUND_TRUTH = (('day21_test.txt', 12),)
    test(GROUND_TRUTH, load_and_run, get_on_after_iterations, 2)
    # RUN
    print('PART 1 result: {}'.format(load_and_run('day21.txt', get_on_after_iterations, 5)))
    print('PART 2 result: {}'.format(load_and_run('day21.txt', get_on_after_iterations, 18)))
