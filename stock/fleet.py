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
    race = models.CharField(max_length=40)
    number = models.IntegerField()
    dammage = models.IntegerField()


class Fleet(models.Model):
    owner = models.ForeignKey(Player, related_name="fleets")
    name = models.CharField(max_length=40)
    compos = models.ManyToManyField(Scheme, through=FleetCompo)
    pos_x = models.IntegerField(default=0)
    pos_y = models.IntegerField(default=0)
    dest_x = models.IntegerField(default=0)
    dest_y = models.IntegerField(default=0)
    militarian = models.BooleanField(default=True)
    cargo_capacity = models.IntegerField(default=0)
    behaviour = models.CharField(max_length=40, default="neutral")
    target = models.IntegerField(default=-1)
    spa_attack = models.IntegerField(default=0)
    pla_attack = models.IntegerField(default=0)
    velocity = models.IntegerField(default=10)
    syst_scan = models.IntegerField(default=0)
    fleet_scan = models.IntegerField(default=0)
    build_order = models.ForeignKey(Scheme, default=None, null=True)
    size = models.CharField(max_length=40)

    @staticmethod
    def generate():
        pass
