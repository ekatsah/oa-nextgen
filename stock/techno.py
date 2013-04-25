# -*- coding: utf-8 -*-
#
# Copyright 2013, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.db import models


class TechnoMerch(models.Model):
    techno = models.ForeignKey("Techno")
    merch = models.CharField(max_length=40)
    amount = models.IntegerField(default=1)


class Techno(models.Model):
    name = models.CharField(max_length=40, unique=True)
    parent = models.ForeignKey('self', null=True)
    prod_merch = models.CharField(max_length=40)
    extract = models.IntegerField(default=0)
    advance_extract = models.ImageField(default=0)
    propeller = models.IntegerField(default=0)
    syst_scan = models.IntegerField(default=0)
    fleet_scan = models.IntegerField(default=0)
    cargo = models.IntegerField(default=0)
    yot = models.IntegerField(default=0)
    scm = models.IntegerField(default=0)
    colo = models.BooleanField(default=False)
    schield = models.IntegerField(default=0)
    type = models.CharField(max_length=40)
    cost_prod = models.IntegerField(default=1)
    cost_ore = models.IntegerField(default=0)
    cost_research = models.IntegerField(default=0)
    structural = models.IntegerField(default=0)
    militarian = models.BooleanField(default=True)
    public = models.BooleanField(default=False)

    @staticmethod
    def generate():
        T = Techno.objects.create
        mine1 = T(name="Mine I", extract=1, type="building", cost_prod=10, 
                  cost_ore=1, structural=10, public=1)

        mine2 = T(name="Mine 2", parent=mine1, extract=2, type="building", 
                  cost_prod=20, cost_ore=1, structural=15, cost_research=100)

    @staticmethod
    def get_publics():
        return Techno.objects.filter(public=True)

