#/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 PART 1
 A similar version of the processor of day 18 is running. The instructions
 used are the following:
 - set X Y : sets the register X to the value Y
 - sub X Y : decreases the register X by the value of Y
 - mul X Y : multiplies the register X by the value of Y
 - jnz X Y : jumps with an offset of Y only if X is not zero.
 Registers between 'a' and 'h' are used, all start at zero. How many times is
 the 'mul' instruction invoked.
 PART 2
 Register 'a' starts at 1. What's the final value of h?
"""

import day18

class Processor(day18.Duet):
    def __init__(self, instructions):
        super().__init__(instructions)
        # override the registers used
        self.mul_counter = 0
        self.reg = { key: 0 for key in 'abcdefgh' }

    def sub(self, x, y):
        """ execute sub command """
        self.reg[x] -= self.value(y)

    def jnz(self, x, y):
        """ execute jnz command """
        if self.value(x) != 0:
            self.counter += self.value(y) - 1

    def execute(self, instruction):
        """ execute an instruction """
        print(self.counter)
        command, *args = instruction.rstrip().split(' ')
        ret = None
        # Execute command
        if command == 'set':
            ret = self.set(*args)
        elif command == 'sub':
            ret = self.sub(*args)
        elif command == 'mul':
            ret = self.mul(*args)
        elif command == 'jnz':
            ret = self.jnz(*args)
        self.counter += 1
        return ret

def get_number_mul(lines):
    """ get the number of times the 'mul' instruction is executed """
    class ProcessorPartOne(Processor):
        def __init__(self, instructions):
            super().__init__(instructions)
            self.mul_counter = 0

        def mul(self, x, y):
            """ execute mul command """
            self.mul_counter += 1
            super().mul(x, y)

    processor = ProcessorPartOne(lines)
    processor.run()
    return processor.mul_counter

def get_final_value_h(lines):
    """ get the final value of register 'h' """
    class ProcessorPartTwo(Processor):
        def __init__(self, instructions):
            super().__init__(instructions)
            self.reg['a'] = 1

    # TODO: must optimize program
    processor = ProcessorPartTwo(lines)
    processor.run()
    return processor.reg['h']

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

if __name__ == "__main__":
    # RUN
    #print('PART 1 result: {}'.format(load_and_run('day23.txt', get_number_mul)))
    print('PART 2 result: {}'.format(load_and_run('day23.txt', get_final_value_h)))
