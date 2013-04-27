# -*- coding: utf-8 -*-
#
# Copyright 2013, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.test import TestCase
from stock.models import Planet, System, Asset, Player

class PlanetTestCase(TestCase):
    def setUp(self):
        self.system = System.objects.create(x=0, y=0)
        self.player = Player.objects.create(name="test")
        self.asset = Asset.objects.create(system=self.system, name="mouh",
                                          owner=self.player)

    def test_planet_base(self):
        """check if is it possible to create planet"""
        pla = Planet.objects.create(system=self.system, asset=self.asset,
                                     position=0)
        self.assertIsInstance(pla, Planet)

    def test_check_popmax(self):
        """check if popmax computing is ok"""
        pla = Planet.objects.create(system=self.system, asset=self.asset,
                                     position=0, radiation=20, temperature=30,
                                     size=2)
        self.assertEqual(pla.get_popmax("wougzy"), 2130)
        self.assertEqual(pla.get_popmax("human"), 2017)
        self.assertEqual(pla.get_popmax("mutant"), 1466)

    def test_check_all_popmax(self):
        """check if all popmax is availible"""
        pla = Planet.objects.create(system=self.system, asset=self.asset,
                                     position=0, radiation=100, temperature=50,
                                     size=2)
        raise Exception(str(pla.get_pops_available()))
