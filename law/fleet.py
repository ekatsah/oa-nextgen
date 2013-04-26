# -*- coding: utf-8 -*-
#
# Copyright 2013, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django import forms
from django.db import models
from django.views.generic.edit import CreateView
from stock.models import Fleet
from command import Command


class MoveFleet(Command):
    fleet = models.ForeignKey(Fleet, related_name="move_to", null=False)
    dest_x = models.IntegerField()
    dest_y = models.IntegerField()
    behaviour = models.CharField(max_length=40)

    def resolv(self):
        fleet.dest_x = self.dest_x
        fleet.dest_y = self.dest_y
        fleet.behaviour = self.behaviour

    def __str__(self):
        args = (Command.__str__(self), self.fleet.name, self.dest_x, 
                self.dest_y, self.beehaviour)
        return "MoveFleet: base(%s), fleet = '%s' -> (%d:%d) in %s" % args
