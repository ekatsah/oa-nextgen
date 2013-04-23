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
    size = randint(3, 6)
    components = [(choice(letters1), choice(letters2)) for _ in xrange(size)]
    word = reduce(lambda a, b: a[0] + a[1] + b[0] + b[1], components)
    return word.capitalize()
