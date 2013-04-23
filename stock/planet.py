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
    system = models.ForeignKey(System)
    asset = models.ForeignKey(Asset)
    position = models.IntegerField()
    size = models.IntegerField()
    gravity = models.IntegerField()
    radiation = models.IntegerField()
    structure = models.IntegerField()
    terra = models.IntegerField()
    taxe = models.IntegerField()
    stability = models.IntegerField()
    ore = models.IntegerField()
    revolt = models.BooleanField()
