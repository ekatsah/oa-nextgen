# -*- coding: utf-8 -*-
#
# Copyright 2013, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.db import models
from game.config import GALAXY_BOUND, SYSTEM_QUANTITY
from random import randint

class System(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()

    @staticmethod
    def generate():
        for _ in xrange(SYSTEM_QUANTITY):
            x, y = 0, 0
            while System.objects.filter(x=x, y=y).count() > 0:
                x = randint(-GALAXY_BOUND, GALAXY_BOUND)
                y = randint(-GALAXY_BOUND, GALAXY_BOUND)
            System.objects.create(x=x, y=y)
