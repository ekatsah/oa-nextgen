# -*- coding: utf-8 -*-
#
# Copyright 2013, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.test import TestCase
from stock.models import Fleet, Player
from law.fleet import MoveFleet


class FleetTestCase(TestCase):
    def setUp(self):
        self.player = Player.objects.create(name="Dummy")

    def test_mvfleet(self):
        """update features of techno"""
        fleet = Fleet.objects.create(name="fleet1", owner=self.player, pos_x=0,
                                     pos_y=0, dest_x=0, dest_y=0)
        self.assertEqual(fleet.dest_x, 0)
        self.assertEqual(fleet.dest_y, 0)
        mv = MoveFleet(fleet=fleet, dest_x=13, dest_y=5)
        mv.resolv()
        self.assertEqual(fleet.dest_x, 13)
        self.assertEqual(fleet.dest_y, 5)
