# -*- coding: utf-8 -*-
#
# Copyright 2013, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.db import models
from game.config import GALAXY_BOUND
from game.feature import FeatureFactory
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
    compos = models.ManyToManyField(Scheme, through=FleetCompo, related_name="is_in")
    pos_x = models.IntegerField(default=GALAXY_BOUND + 10)
    pos_y = models.IntegerField(default=GALAXY_BOUND + 10)
    dest_x = models.IntegerField(default=GALAXY_BOUND + 10)
    dest_y = models.IntegerField(default=GALAXY_BOUND + 10)

    # Features
    militarian = models.BooleanField(default=False)
    cargo_capacity = models.IntegerField(default=0)
    behaviour = models.CharField(max_length=40, default="neutral")
    target = models.IntegerField(default=0)
    spa_attack = models.IntegerField(default=0)
    pla_attack = models.IntegerField(default=0)
    velocity = models.IntegerField(default=-1)
    syst_scan = models.IntegerField(default=0)
    fleet_scan = models.IntegerField(default=0)
    build_order = models.ForeignKey(Scheme, default=None, null=True, related_name="built_by")
    size = models.CharField(max_length=40)

    features = FeatureFactory("size", "poc", "velocity", "spa_attack",
                              "pla_attack", "syst_scan", "fleet_scan",
                              "cargo", "scm", "colo", "shield", "public",
                              "cost_prod", "cost_ore", "militarian")
