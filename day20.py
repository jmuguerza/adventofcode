#/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 PART 1
 The input is a buffer listing particles in order, each with coordinates
 for the position, velocity and acceleration. Each tick, the particles
 are updated simultaneously: increase X velocity by X acceleration; same for
 Y, and Z. Finally, update the positions in the same fashion. GPU would like
 to know which particle is closest to 0,0,0 (in Manhattan distance) in the
 long term. In the LONG TERM, we can consider that the particle closest to zero
 will be the one with the smallest acceleration, and smallest speed.
 PART 2
 Particles that are at the same place at the same time, collide. How many
 particles are left after all collisions are resolved?
"""

import re
import math
from itertools import combinations
from collections import defaultdict

class Particle(object):
    """ class to represent a particle """
    def __init__(self, pos, vel, acc):
        self.pos_0 = pos
        self.vel_0 = vel
        self.acc_0 = acc
        self.pos = pos
        self.vel = vel
        self.acc = acc

    @staticmethod
    def manhattan(vector):
        """ Return the manhattan distance """
        return sum(map(abs, vector))

    @staticmethod
    def constant_vel(vel, acc):
        """ Get the manhattan distance of the velocity component that
        remains unchanged by the acceleration """
        return Particle.manhattan(list(vel[i] for i in range(len(acc)) if acc[i] == 0))

    @staticmethod
    def add(a, b):
        """ add two vectors """
        return tuple(a[i] + b[i] for i in range(len(a)))

    def step(self):
        """ make a step and return the position """
        self.vel = Particle.add(self.vel, self.acc)
        self.pos = Particle.add(self.pos, self.vel)
        return self.pos

def parse_line(line):
    """ Parse a line and return pos, vel, and acc """
    numbers = re.findall('[-0-9]+', line)
    if len(numbers) < 9:
        return None
    pos = tuple(map(int, numbers[0:3]))
    vel = tuple(map(int, numbers[3:6]))
    acc = tuple(map(int, numbers[6:9]))
    return pos, vel, acc

def get_collisions(lines):
    """ get the number of collisions in the long term """
    # Instantiate all particles
    num_collisions = 0
    particles = [ Particle(*parse_line(line)) for line in lines ]
    # TODO: this is not the best approach, since we don't know at which
    # iteration we'll guarantee that there will be no more collisions. 
    # A more exact method would be to solve the equation P1(n) = P2(n)
    # for every possible combination of particles, and then delete the 
    # ones that collide on a chronological order (two particles may eventually
    # collide, but if one of them is deleted because it collides with a 
    # third, then they will never collide). 
    for i in range(1000):
        positions = defaultdict(list)
        # Get all positions
        for _ in ( positions[p.step()].append(p_num) for p_num, p in enumerate(particles) ): pass
        collisions = []
        # Get all collisions
        for _ in map(collisions.extend, ( val for val in positions.values() if len(val) > 1 )): pass
        # Delete particles
        for particle in sorted(collisions, reverse=True):
            del(particles[particle])
        num_collisions += len(collisions)
        # TODO: Break condition? This is actually quite hard, since we should
        # consider that no more collisions will happen when all pairs of
        # are increasing in velocity AND increasing the distance between each other
    return len(particles)

def get_closest_to_zero(lines):
    """ get the particle closest to zero in the long term """
    min_particle = None
    min_acc_mht = None
    min_constant_vel = None
    for particle_num, line in enumerate(lines):
        pos, vel, acc = parse_line(line)
        this_acc_mht = Particle.manhattan(acc)
        if min_acc_mht is None:
            min_acc_mht = this_acc_mht
            min_particle = particle_num
            min_constant_vel = Particle.constant_vel(vel, acc)
        elif this_acc_mht < min_acc_mht:
            # If it's smaller, then it'll be the one that drifts away from zero
            # at the slowest speed.
            min_acc_mht = this_acc_mht
            min_particle = particle_num
            min_constant_vel = Particle.constant_vel(vel, acc)
        elif this_acc_mht == min_acc_mht:
            # If they have the same acceleration, then, check the speed.
            this_constant_vel = Particle.constant_vel(vel,acc)
            if this_constant_vel < min_constant_vel:
                min_acc_mht = this_acc_mht
                min_particle = particle_num
                min_constant_vel = this_constant_vel
            elif this_constant_vel == min_constant_vel:
                # TODO: should consider initial position and velocity
                pass
    return min_particle

def load_and_run(filename, func):
    """ Load the file and run the function """
    with open(filename) as f:
        lines = f.read().splitlines()
    return func(lines)

def test(truth, check_function, *args):
    for test_input, result in truth:
        try:
            assert(check_function(test_input, *args) == result)
        except AssertionError:
            print("Error trying to assert {}({}) == {}".format(
                    check_function.__name__, test_input, result))

if __name__ == "__main__":
    # Test for PART 1
    GROUND_TRUTH = (('day20_test.txt', 0),)
    test(GROUND_TRUTH, load_and_run, get_closest_to_zero)
    # Test for PART 2
    GROUND_TRUTH = (('day20_test2.txt', 1),)
    test(GROUND_TRUTH, load_and_run, get_collisions)
    # RUN
    print('PART 1 result: {}'.format(load_and_run('day20.txt', get_closest_to_zero)))
    print('PART 2 result: {}'.format(load_and_run('day20.txt', get_collisions)))
