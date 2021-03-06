# -*- coding: utf-8 -*-
#
# Copyright 2013, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.db import models
from game.feature import FeatureFactory
from weapon import Weapon


class TechnoMerch(models.Model):
    techno = models.ForeignKey("Techno")
    merch = models.CharField(max_length=40)
    amount = models.IntegerField(default=1)


class Techno(models.Model):
    name = models.CharField(max_length=40, unique=True)
    parent = models.ForeignKey('self', null=True)
    weapon = models.ForeignKey(Weapon, null=True, default=None, related_name="used_by")
    type = models.CharField(max_length=40, default="")

    # Feature    
    prod_merch = models.CharField(max_length=40, default="")
    extract = models.IntegerField(default=0)
    advance_extract = models.IntegerField(default=0)
    propeller = models.IntegerField(default=0)
    syst_scan = models.IntegerField(default=0)
    fleet_scan = models.IntegerField(default=0)
    cargo = models.IntegerField(default=0)
    yot = models.IntegerField(default=0)
    scm = models.IntegerField(default=0)
    colo = models.BooleanField(default=False)
    shield = models.IntegerField(default=0)
    cost_prod = models.IntegerField(default=0)
    cost_ore = models.IntegerField(default=0)
    cost_research = models.IntegerField(default=0)
    structural = models.IntegerField(default=0)
    militarian = models.BooleanField(default=False)
    public = models.BooleanField(default=False)

    features = FeatureFactory("prod_merch", "extract", "advance_extract",
                              "propeller", "syst_scan", "fleet_scan",
                              "cargo", "yot", "scm", "colo", "shield",
                              "cost_prod", "cost_ore", "structural",
                              "militarian", "public")

    @staticmethod
    def get_publics():
        return Techno.objects.filter(public=True)
