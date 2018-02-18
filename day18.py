#/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 PART 1
 Decipher assembly code. Registers are named with a single
 letter and can hold a single integer.
 * snd X : plays sound with frequency equal to X
 * set X Y : sets register X to Y
 * add X Y : increases the register X by the value Y
 * mul X Y : multiplies X by Y, sets value to X
 * mod X Y : sets X to remainder of X/Y
 * rcv X : recovers last sound played in X, only when X is not zero
 * jgz X Y : jumps offset Y only if X is greater than zero
 What is the value of the recovered frequency the first time a rcv instruction is 
 executed with a non-zero value?
 PART 2
 Actually, programs are run by two entities at the same time. 'snd X' sends
 the value of X to the other program. 'rcv X' receives the next value and 
 stores it in register X. If no values are in the queue, it blocks. Each program
 has a program ID; the register p should begin with this value. If both programs
 are deadlocked, they terminate. How many times program '1' sent a value?
"""

from itertools import count
from threading import Thread
from queue import Queue, Empty

class Duet(object):
    """ Class for the Duet object, with instructions and registers """
    def __init__(self, instructions):
        self.reg = { key: 0 for key in 'abcdefghijklmnopqrstuvwxyz' }
        self.last_played = 0
        self.counter = 0
        self.instructions = instructions

    def value(self, x):
        """ Get the value of a register or number """
        try:
            return int(x)
        except ValueError:
            return self.reg[x]

    def snd(self, x):
        """ execute snd command """
        self.last_played = self.value(x)

    def set(self, x, y):
        """ execute set command """
        self.reg[x] = self.value(y)

    def add(self, x, y):
        """ execute add command """
        self.reg[x] += self.value(y)

    def mul(self, x, y):
        """ execute mul command """
        self.reg[x] *= self.value(y)

    def mod(self, x, y):
        """ execute mod command """
        self.reg[x] = self.value(x) % self.value(y)

    def rcv(self, x):
        """ execute rcv command """
        if self.value(x):
            return self.last_played
        return None

    def jgz(self, x, y):
        """ execute jgz command """
        if self.value(x) > 0:
            self.counter += self.value(y) - 1

    def execute(self, instruction):
        """ execute an instruction """
        command, *args = instruction.rstrip().split(' ')
        ret = None
        # Execute command
        if command == 'snd':
            ret = self.snd(*args)
        elif command == 'set':
            ret = self.set(*args)
        elif command == 'add':
            ret = self.add(*args)
        elif command == 'mul':
            ret = self.mul(*args)
        elif command == 'mod':
            ret = self.mod(*args)
        elif command == 'rcv':
            ret = self.rcv(*args)
        elif command == 'jgz':
            ret = self.jgz(*args)

        self.counter += 1

        return ret

    def run(self):
        """ Start execution """
        while (self.counter < len(self.instructions)):
            self.execute(self.instructions[self.counter])


def load_and_run(filename, func):
    """ Load the file and run the function """
    with open(filename) as f:
        instructions = f.readlines()
    return func(instructions)

def get_recover(program):
    """ Return the first value recovered by recover function """
    class DuetPartOne(Duet):
        def run(self):
            """ Start execution """
            while (self.counter < len(self.instructions)):
                ret = self.execute(self.instructions[self.counter])
                if ret is not None:
                    return ret
    duet = DuetPartOne(program)
    return duet.run()

def get_send_program_1(program):
    """ Return the number of times program '1' sent a value """
    class DuetPartTwo(Duet):
        ids = count(0)
        def __init__(self, instructions):
            super().__init__(instructions)
            self.id = next(self.ids)
            self.reg['p'] = self.id
            self.queue = Queue()
            self.other = None
            self.receiving = False
            self.terminate = False
            self.sent = 0

        def set_other(self, other):
            """ Set the other program """
            self.other = other

        def snd(self, x):
            """ Send the value to the other program """
            if self.other:
                self.other.queue.put(self.value(x))
                self.sent += 1

        def rcv(self, x):
            """ Receive the value from the queue """
            # If the other is blocking and the queue is empty, terminate
            self.receiving = True
            while True:
                try:
                    self.reg[x] = self.queue.get(timeout=1)
                    break
                except Empty:
                    # Check if the other thread is blocked too
                    if self.other.receiving and self.other.queue.empty():
                        self.terminate = True
                        return 
            self.receiving = False

        def run(self):
            """ Start execution """
            while (not self.terminate and self.counter < len(self.instructions)):
                self.execute(self.instructions[self.counter])

    duet_0 = DuetPartTwo(program)
    duet_1 = DuetPartTwo(program)

    duet_1.set_other(duet_0)
    duet_0.set_other(duet_1)

    # Start threads
    duet_0_t = Thread(target=duet_0.run)
    duet_1_t = Thread(target=duet_1.run)
    duet_0_t.start()
    duet_1_t.start()

    duet_0_t.join()
    duet_1_t.join()

    return duet_1.sent

def test(truth, check_function, *args):
    for test_input, result in truth:
        try:
            assert(check_function(test_input, *args) == result)
        except AssertionError:
            print("Error trying to assert {}({}) == {}".format(
                    check_function.__name__, test_input, result))

if __name__ == "__main__":
    # Test for PART 1
    GROUND_TRUTH = (('day18_test.txt', 4),)
    test(GROUND_TRUTH, load_and_run, get_recover)
    # RUN
    print('PART 1 result: {}'.format(load_and_run('day18.txt', get_recover)))
    print('PART 2 result: {}'.format(load_and_run('day18.txt', get_send_program_1)))
