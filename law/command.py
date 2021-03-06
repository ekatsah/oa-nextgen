# -*- coding: utf-8 -*-
#
# Copyright 2013, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.db import models
from stock.models import Player


class Command(models.Model):
    player = models.ForeignKey(Player, null=True, blank=True)
    date = models.DateTimeField(auto_now=True)
    week = models.IntegerField(default=0)
#    source = models.IPAddressField(dea)

    class Meta:
        abstract = True

    def __str__(self):
        if self.player:
            args = (self.player.name, self.player.id, str(self.date), self.week)
        else:
            args = ("None", -1, str(self.date), self.week)

        return "RawCom, player %s (%d), at %s on week %d" % args 

    def __repr__(self):
        return self.__str__()