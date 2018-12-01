#/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 PART 1
 A tower contains a disc with programs. The first program of the 
 tower also contains a disc with subtowers, also containing programs,
 an so on. The name of each of the programs contained by each disc,
 as well as their weight, and the programs contained above is known.
 Get the root program.
 PART 2
 One program has the wrong weight, making the towers unbalanced. What
 would its weight need to be?
"""
import pprint
import re
from collections import defaultdict

REGEX = r'([a-z]+) \(([0-9]+)\)(?: -> )?(.*)?'
REGEX_CHILDREN = r'([a-z]+)(?:, )?'

def load_and_run(filename, func):
    """ Load the file and run the function """
    with open(filename) as f:
        tower = defaultdict(dict)
        for name, weight, rest in re.findall(REGEX, f.read()):
            children = re.findall(REGEX_CHILDREN, rest)
            tower[name].update(weight=int(weight), children=children)
            for child in children:
                tower[child].update(parent=name)
    return func(tower)

def get_root(tower):
    """ Get the root of tree """
    # We are sure that there is only one without parent
    return list(filter(
            lambda x: False if 'parent' in x[1] else True,
            list(tower.items())
            ))[0][0]

def update_weights(tower, root):
    """ Update the weights, starting from root """
    # Save the original weight
    for child in tower[root]['children']:
        tower[child]['original_weight'] = tower[child]['weight']
        update_weights(tower, child)
        tower[root]['weight'] += tower[child]['weight']

def get_wrong_weight(tower, root, diff):
    """ Get the wrong weight, and difference between the children of root """
    weights = [ tower[child]['weight'] for child in tower[root]['children'] ]
    # If all weights are equal, or no children then this is the problem
    if len(set(weights)) <= 1:
        return root, diff
    # Else, keep iterating
    wrong_weight, correct_weight = sorted(set(weights), key=weights.count)
    next_root = list(filter(
            lambda x: True if tower[x]['weight'] == wrong_weight else False,
            tower[root]['children']))[0]
    return get_wrong_weight(tower, next_root, correct_weight - wrong_weight)

def get_needed_weight(tower):
    """ Get the root of tree """
    root = get_root(tower)
    # So far, we don't have the cumulative weights. Get them
    update_weights(tower, root)
    # Get the child of root that has a different cumulative weight
    name, diff = get_wrong_weight(tower, root, 0)
    # Return
    return tower[name]['original_weight'] + diff


def test(truth, check_function, *args):
    for test_input, result in truth:
        try:
            assert(check_function(test_input, *args) == result)
        except AssertionError:
            print("Error trying to assert {}({}) == {}".format(
                    check_function.__name__, test_input, result))

if __name__ == "__main__":
    # Test for PART 1
    GROUND_TRUTH = (('day7_test.txt', 'tknk'),)
    test(GROUND_TRUTH, load_and_run, get_root)
    # Test for PART 2
    GROUND_TRUTH = (('day7_test.txt', 60),)
    test(GROUND_TRUTH, load_and_run, get_needed_weight)
    # RUN
    print('PART 1 result: {}'.format(load_and_run('day7.txt', get_root)))
    print('PART 2 result: {}'.format(load_and_run('day7.txt', get_needed_weight)))
