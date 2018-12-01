#/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 PART 1
 We receive a stream of characters. {} delimit groups. A group can
 contain another groups, or garbage, delimited by <>. Any character
 can be found inside the garbage, including {}. Characters after ! 
 should be ignored. Each group receives a score, which is one more 
 than the group that immediately contains it (outermost has value 1).
 Get total score.
 PART 2
 Count the number of non cancelled characters inside the garbage.
"""


def load_and_run(filename, func):
    """ Load the file and run the function """
    with open(filename) as f:
        return func(f.read())

def get_total_score_and_garbage(stream):
    """ Return the total score for the stream of characters """
    garbage = False
    depth = 0
    total_score = 0
    total_garbage = 0
    iterator = iter(stream)
    for char in iterator:
        if char == '!':
            # Discard next character
            next(iterator)
            continue
        elif garbage and char == '>':
            garbage = False
            continue
        elif garbage and char != '>':
            total_garbage += 1
            continue
        elif char == '<':
            garbage = True
            continue
        elif char == '{':
            depth += 1
            continue
        elif char == '}':
            total_score += depth
            depth -= 1
            continue
    return total_score, total_garbage


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
            ('{}', (1,0)),
            ('{{{}}}', (6,0)),
            ('{{},{}}', (5,0)),
            ('{{{},{},{{}}}}', (16,0)),
            ('{<a>,<a>,<a>,<a>}', (1,4)),
            ('{{<ab>},{<ab>},{<ab>},{<ab>}}', (9,8)),
            ('{{<!!>},{<!!>},{<!!>},{<!!>}}', (9,0)),
            ('{{<a!>},{<a!>},{<a!>},{<ab>}}', (3,17))
    )
    test(GROUND_TRUTH, get_total_score_and_garbage)
    # RUN
    total_score, total_garbage = load_and_run('day9.txt', get_total_score_and_garbage)
    print('PART 1 result: {}'.format(total_score))
    print('PART 2 result: {}'.format(total_garbage))
