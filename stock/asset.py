# -*- coding: utf-8 -*-
#
# Copyright 2013, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.db import models
from game.utils import randname
from system import System
from player import Player

class Asset(models.Model):
    system = models.ForeignKey(System, related_name="assets")
    name = models.CharField(max_length="40")
    owner = models.ForeignKey(Player, related_name="assets")

    @staticmethod
    def generate():
        neutral = Player.objects.get(name="Void")
        for system in System.objects.all():
            Asset.objects.create(system=system, name=randname(), owner=neutral)
