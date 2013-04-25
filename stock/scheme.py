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
from techno import Techno


class SchemeCompo(models.Model):
    scheme = models.ForeignKey("Scheme")
    techno = models.ForeignKey(Techno)
    number = models.IntegerField()


class SchemeFeature(ManyFeature):
    scheme = models.ForeignKey("Scheme")


class SchemeMerch(ManyFeature):
    scheme = models.ForeignKey("Scheme")


class Scheme(models.Model):
    owner = models.ForeignKey(Player, related_name="schemes")
    compos = models.ManyToManyField(Techno, through=SchemeCompo)
    features = models.ManyToManyField(Feature, through=SchemeFeature)
    merch = models.ManyToManyField(Feature, through=SchemeMerch,
                                   related_name="schemes_contains")
    name = models.CharField(max_length=40)
    brand = models.CharField(max_length=40)
    domain = models.ForeignKey(Feature, related_name="schemes_in_domain")
    
    @staticmethod
    def generate():
        pass
