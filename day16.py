#/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 PART 1
 Sixteen programs are dancing, named from 'a' to 'p'. The dance
 consists of a sequence of moves: spin, produces a left shift,
 exchange, a swap of places, and partners, too. What's the order
 at the end?
 PART 2
 They dance a total of one billion times. 
"""

from collections import deque

PROGRAMS = 'abcdefghijklmnop'

def spin(programs, inst):
    """ Spin the list of programs """
    rotated = deque(programs)
    rotated.rotate(int(inst))
    return ''.join(rotated)

def exchange(programs, inst):
    """ Exchange two indices """
    a, b = map(int, inst.split('/'))
    return ''.join([ 
        programs[a] if i == b else
        programs[b] if i == a else
        programs[i] for i in range(len(programs))])

def partner(programs, inst):
    """ Exchange two programs """
    a, b = inst.split('/')
    return exchange(programs, "{}/{}".format(
        programs.index(a), programs.index(b)))

def get_final_position(moves, programs, n_times=1):
    """ Dance and get final position """
    for n in range(n_times):
        for move in moves.split(','):
            programs = ( 
                    spin(programs, move[1:]) if move[0] == 's' else
                    exchange(programs, move[1:]) if move[0] == 'x' else
                    partner(programs, move[1:]) if move[0] == 'p' else
                    programs)
    return programs

def load_and_run(filename, func, **args):
    """ Load instructions and run function """
    with open(filename) as f:
        return func(f.read().rstrip(), **args)

def test(truth, check_function, *args):
    for test_input, result in truth:
        try:
            my_result = check_function(test_input, *args)
            assert(my_result == result)
        except AssertionError:
            print("Error trying to assert {}({}) == {} != {}".format(
                    check_function.__name__, test_input, my_result, result))

if __name__ == "__main__":
    # Test for PART 1
    GROUND_TRUTH = (
            ("s1,x3/4,pe/b", "baedc"),
    )
    test(GROUND_TRUTH, get_final_position, "abcde")
    # Test for PART 2
    GROUND_TRUTH = (
            ("s1,x3/4,pe/b", "ceadb"),
    )
    test(GROUND_TRUTH, get_final_position, "abcde", 2)
    # RUN
    print('PART 1 result: {}'.format(load_and_run('day16.txt', get_final_position, programs=PROGRAMS, n_times=1)))
    print('PART 2 result: {}'.format(load_and_run('day16.txt', get_final_position, programs=PROGRAMS, n_times=1000000000)))
