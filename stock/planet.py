# -*- coding: utf-8 -*-
#
# Copyright 2013, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.db import models
from math import log, log1p, exp, floor
from game.config import RACES
from system import System
from asset import Asset


class PlanetPop(models.Model):
    planet = models.ForeignKey("Planet", related_name="pops")
    race = models.CharField(max_length=40)
    pop = models.IntegerField(default=20)
    popmax = models.IntegerField()
    growth = models.IntegerField()


class Planet(models.Model):
    system = models.ForeignKey(System, related_name="planets")
    asset = models.ForeignKey(Asset, related_name="planets")
    position = models.IntegerField()
    size = models.IntegerField(default=0)
    temperature = models.IntegerField(default=-1)
    radiation = models.IntegerField(default=-1)
    structure = models.IntegerField(default=0)
    terra = models.IntegerField(default=0)
    taxe = models.IntegerField(default=-1)
    stability = models.IntegerField(default=-1)
    ore = models.IntegerField(default=-1)
    revolt = models.BooleanField(default=False)

    def pops(self):
        return PlanetPop.objects.filter(planet=self)

    def get_pops_available(self):
        tmp = {race: self.get_popmax(race) for race in RACES}
        return tmp
    #{race: popmax for race, popmax in tmp.iteritems() if popmax > 0}

    def get_popmax(self, race):
        rc, t, r = RACES[race], self.temperature, self.radiation
        te, tm = (rc[0][1] - rc[0][0])/2, (rc[0][1] + rc[0][0])/2
        re, rm = (rc[1][1] - rc[1][0])/2, (rc[1][1] + rc[1][0])/2
        ta = tm / (te * (abs(tm - t) + 41))
        ra = rm / (re * (abs(rm - r) + 41))
        pmax = 5000*log1p(self.size)*exp(10*ta*ra)*(1+self.terra)/log(re+te)
        return int(pmax * (11 - self.pops.count() / 10) / 10)
