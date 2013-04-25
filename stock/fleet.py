# -*- coding: utf-8 -*-
#
# Copyright 2013, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.db import models
from game.feature import Feature, ManyFeature
from player import Player
from scheme import Scheme


class FleetCompo(models.Model):
    fleet = models.ForeignKey("Fleet")
    scheme = models.ForeignKey(Scheme)
    race = models.ForeignKey(Feature)
    number = models.IntegerField()
    dammage = models.IntegerField()


class FleetFeature(ManyFeature):
    fleet = models.ForeignKey("Fleet")


class FleetCargo(ManyFeature):
    fleet = models.ForeignKey("Fleet")


class Fleet(models.Model):
    owner = models.ForeignKey(Player, related_name="fleets")
    name = models.CharField(max_length=40)
    compos = models.ManyToManyField(Scheme, through=FleetCompo)
    pos_x = models.IntegerField()
    pos_y = models.IntegerField()
    dest_x = models.IntegerField()
    dest_y = models.IntegerField()
    features = models.ManyToManyField(Feature, through=FleetFeature)
    cargos = models.ManyToManyField(Feature, through=FleetCargo,
                                    related_name="in_fleets")

    @staticmethod
    def generate():
        pass
