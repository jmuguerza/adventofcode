#/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 PART 1
 Passphrases must be checked for validity. One passphrase
 is valid if no duplicate words are in it. Check how many
 of the passphrases provided are valid.
 PART 2
 For a passphrase to be valid, not two anagrams must exist.
"""

FILENAME = 'day4.txt'

import itertools

def check_duplicate(passphrase):
    """ Check if a passphrase does not contains duplicates """
    if not passphrase:
        return False
    if len(list(passphrase.split())) != len(set(passphrase.split())):
        return False
    return True

def check_anagram(passphrase):
    """ Check if a passphrase does not contains anagrams """
    if not passphrase:
        return False
    anagrams = [
            tuple(sorted(word))
            for word in passphrase.split()
    ]
    if len(anagrams) != len(set(anagrams)):
        return False
    return True

def check_passphrases(filename, check_function):
    """ Check how many valid passphrases are in a file """
    valid = 0
    with open(filename) as f:
        for passphrase in f.read().split('\n'):
            if not check_function(passphrase):
                continue
            valid += 1
    return valid

def test(truth, check_function):
    for passphrase, result in truth:
        try:
            assert(check_function(passphrase) == result)
        except AssertionError:
            print("Error trying to assert {}({}) == {}".format(
                    check_function.__name__, passphrase, result))

if __name__ == "__main__":
    # Test for PART 1
    GROUND_TRUTH = (
            ('aa bb cc dd ee', True),
            ('aa bb cc dd aa', False),
            ('aa bb cc dd aaa', True),
    )
    test(GROUND_TRUTH, check_duplicate)
    # Test for PART 2
    GROUND_TRUTH = (
            ('abcde fghij', True),
            ('abcde xyz ecdab', False),
            ('a ab abc abd abf abj', True),
            ('iiii oiii ooii oooi oooo', True),
            ('oiii ioii iioi iiio', False),
    )
    test(GROUND_TRUTH, check_anagram)
    # RUN
    print('PART 1 result: {}'.format(check_passphrases(FILENAME, check_duplicate)))
    print('PART 2 result: {}'.format(check_passphrases(FILENAME, check_anagram)))
