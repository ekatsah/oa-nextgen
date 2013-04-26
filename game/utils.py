# -*- coding: utf-8 -*-
#
# Copyright 2013, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from random import choice, randint

def randname():
    letters1 = "aaeeiioouuy"
    letters2 = "zrrttppqsssddfghjkllmmwxccvbbnn"
    size = randint(3, 5)
    components = [choice(letters1) + choice(letters2) for _ in xrange(size)]
    word = reduce(lambda a, b: a + b, components)
    if randint(0, 2) != 2:
        word = choice(letters2) + word
    return word.capitalize()

def struct2size(points):
    #        1  2   3   4   5    6    7    8     9 -> 10
    sizes = [2, 5, 10, 20, 50, 100, 250, 500, 1000]
    for size, struct in enumerate(sizes):
        if points <= struct:
            return size + 1
    else:
        return 10

def poc2size(points, spa_attack, pla_attack):
#             1   2    3    4     5     6      7      8       9 -> 10
    sizes = [10, 50, 100, 330, 1500, 5000, 10000, 50000, 100000]
    points = points * 0.6 + spa_attack * 0.4 + pla_attack * 0.1
    for size, struct in enumerate(sizes):
        if points <= struct:
            return size + 1
    else:
        return 10
