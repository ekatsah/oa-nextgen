# -*- coding: utf-8 -*-
#
# Copyright 2013, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.db import models
from player import Player
from techno import Techno


class SchemeCompo(models.Model):
    scheme = models.ForeignKey("Scheme")
    techno = models.ForeignKey(Techno)
    number = models.IntegerField()


class SchemeMerch(models.Model):
    scheme = models.ForeignKey("Scheme")
    merch = models.CharField(max_length=40)
    amount = models.IntegerField(default=1)


class Scheme(models.Model):
    owner = models.ForeignKey(Player, related_name="schemes")
    compos = models.ManyToManyField(Techno, through=SchemeCompo, related_name="is_in")
    name = models.CharField(max_length=40)
    brand = models.CharField(max_length=40)
    domain = models.CharField(max_length=40)
    militarian = models.BooleanField(default=False)
    size = models.IntegerField(default=0)
    poc = models.IntegerField(default=0)
    velocity = models.IntegerField(default=-1)
    cost_prod = models.IntegerField(default=0)
    cost_ore = models.IntegerField(default=0)
    cargo = models.IntegerField(default=0)
    syst_scan = models.IntegerField(default=0)
    fleet_scan = models.IntegerField(default=0)
    scm = models.IntegerField(default=0)
    colo = models.BooleanField(default=False)
    spa_attack = models.IntegerField(default=0)
    pla_attack = models.IntegerField(default=0)
    
    @staticmethod
    def generate():
        pass
