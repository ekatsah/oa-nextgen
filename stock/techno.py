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
    advance_extract = models.IntegerField(default=0)
    propeller = models.IntegerField(default=0)
    syst_scan = models.IntegerField(default=0)
    fleet_scan = models.IntegerField(default=0)
    cargo = models.IntegerField(default=0)
    yot = models.IntegerField(default=0)
    scm = models.IntegerField(default=0)
    colo = models.BooleanField(default=False)
    schield = models.IntegerField(default=0)
    type = models.CharField(max_length=40, default="")
    cost_prod = models.IntegerField(default=0)
    cost_ore = models.IntegerField(default=0)
    cost_research = models.IntegerField(default=0)
    structural = models.IntegerField(default=0)
    militarian = models.BooleanField(default=False)
    public = models.BooleanField(default=False)

    @staticmethod
    def generate():
        T = Techno.objects.create
        mine1 = T(name="Mine I", extract=1, type="building", cost_prod=10, 
                  cost_ore=1, structural=10, public=1)

        mine2 = T(name="Mine II", parent=mine1, extract=2, type="building", 
                  cost_prod=20, cost_ore=1, structural=15, cost_research=100)

        rea1 = T(name="Reactor I", propeller=1, type="component",
                 cost_prod=2, cost_ore=1, structural=1, public=True)

        shield1 = T(name="Shield I", shield=1, type="component",
                    cost_prod=5, cost_ore=1, structural=1, public=True)

        cargo1 = T(name="Cargo I", cargo=10, type="component",
                   cost_prod=2, cost_ore=2, structural=2, parent=rea1)

        scan1 = T(name="Scanner I", syst_scan=1, type="component",
                  cost_prod=10, cost_ore=5, structural=1, parent=rea1)

    @staticmethod
    def get_publics():
        return Techno.objects.filter(public=True)

