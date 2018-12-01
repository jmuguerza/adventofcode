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

class Programs(object):
    def __init__(self, programs):
        self._programs = list(programs)
        self._insts = { 
                's': self._spin,
                'x': self._exchange,
                'p': self._partner
        }

    def exec(self, inst):
        """ Execute one instruction """
        self._insts[inst[0]](inst[1:])

    def _spin(self, inst):
        """ Spin the list of programs """
        n = int(inst)
        self._programs = (self._programs*2)[len(self._programs) - n:2*len(self._programs) - n]

    def _exchange(self, inst):
        """ Exchange two indices """
        a, b = map(int, inst.split('/'))
        self._programs[a], self._programs[b] = self._programs[b], self._programs[a]

    def _partner(self, inst):
        """ Exchange two programs """
        a, b = inst.split('/')
        self._exchange("{}/{}".format(self._programs.index(a), self._programs.index(b)))

    def __str__(self):
        return ''.join(self._programs)

def get_final_position(moves, programs, n_times=1):
    """ Dance and get final position """
    p = Programs(programs)
    moves = moves.split(',') if isinstance(moves, str) else moves
    for n in range(n_times):
        # Check if we ever go back to first state
        if n and str(p) == programs:
            return get_final_position(moves, programs, n_times%n)
        for move in moves:
            p.exec(move)
    return str(p)

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
