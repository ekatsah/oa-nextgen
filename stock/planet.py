# -*- coding: utf-8 -*-
#
# Copyright 2013, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.db import models
from system import System
from asset import Asset

class Planet(models.Model):
    system = models.ForeignKey(System, related_name="planets")
    asset = models.ForeignKey(Asset, related_name="planets")
    position = models.IntegerField()
    size = models.IntegerField(default=0)
    gravity = models.IntegerField(default=-1)
    radiation = models.IntegerField(default=-1)
    structure = models.IntegerField(default=0)
    terra = models.IntegerField(default=0)
    taxe = models.IntegerField(default=-1)
    stability = models.IntegerField(default=-1)
    ore = models.IntegerField(default=-1)
    revolt = models.BooleanField(default=False)
