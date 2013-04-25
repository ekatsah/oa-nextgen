# -*- coding: utf-8 -*-
#
# Copyright 2013, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.db import models


class Weapon(models.Model):
    name = models.CharField(max_length=40, unique=True)
    spa_attack = models.IntegerField(default=0)
    shield_attack = models.IntegerField(default=0)
    pla_attack = models.IntegerField(default=0)
    velocity = models.IntegerField(default=0)
    scope = models.IntegerField(default=0)
    accuracy = models.CommaSeparatedIntegerField(max_length=60)
