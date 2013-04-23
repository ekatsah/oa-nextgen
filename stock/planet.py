# -*- coding: utf-8 -*-
#
# Copyright 2013, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from game.config import PLANET_MIN, PLANET_MAX
from django.db import models
from random import randint
from system import System
from asset import Asset

class Planet(models.Model):
    system = models.ForeignKey(System)
    asset = models.ForeignKey(Asset)
    position = models.IntegerField()
    size = models.IntegerField()
    gravity = models.IntegerField()
    radiation = models.IntegerField()
    structure = models.IntegerField()
    terra = models.IntegerField()
    taxe = models.IntegerField()
    stability = models.IntegerField()
    ore = models.IntegerField()
    revolt = models.BooleanField()

    @staticmethod
    def generate():
        for asset in Asset.objects.all():
            planet_count = randint(PLANET_MIN, PLANET_MAX)
            for position in map(lambda p: p + 1, xrange(planet_count)):
                size = randint(1, 4)
                Planet.objects.create(system=asset.system, asset=asset,
                                      position=position, size=size,
                                      gravity=randint(0, 100),
                                      radiation=randint(0, 100),
                                      structure=size * 20 + randint(0, 30),
                                      terra=0, taxe=2, stability=100,
                                      ore=randint(0, 6),
                                      revolt=False)
