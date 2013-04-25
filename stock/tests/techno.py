# -*- coding: utf-8 -*-
#
# Copyright 2013, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.test import TestCase
from stock.models import Techno

class TechnoTestCase(TestCase):
    def setUp(self):
        pass

    def test_update_feature(self):
        """update features of techno"""
        tech = Techno.objects.create(name="TechTestU1")
        tech.update_feature(public=1, cost_ore=2)
        self.assertEqual(tech.feature("public"), 1)
        self.assertEqual(tech.feature("cost_ore"), 2)
        self.assertEqual(tech.feature("cost_research"), 0)

    def test_update_feature_replace(self):
        """update features and replace, in techno"""
        tech = Techno.objects.create(name="TechTestU2")
        tech.update_feature(public=1, cost_ore=2)
        self.assertEqual(tech.feature("public"), 1)
        self.assertEqual(tech.feature("cost_ore"), 2)
        tech.update_feature(public=3, cost_research=4)
        self.assertNotEqual(tech.feature("public"), 3)
        self.assertEqual(tech.feature("cost_research"), 4)

    def test_get_all_features(self):
        """set features on techno and check all features as a list"""
        tech = Techno.objects.create(name="TechTestFS")
        tech.update_feature(YOT=1, SCM=2)
        for feat in tech.features():
            self.assertTrue((feat["code"] == "YOT") == (feat["value"] == 1))
            self.assertTrue((feat["code"] == "SCM") == (feat["value"] == 2))
            self.assertTrue(feat["code"] == "YOT" or feat["code"] == "SCM")

    def test_get_a_feature(self):
        """set features on techno and check all features one by one"""
        tech = Techno.objects.create(name="TechTestAF")
        tech.update_feature(YOT=1, SCM=2)
        self.assertEqual(tech.feature("YOT"), 1)
        self.assertEqual(tech.feature("SCM"), 2)
