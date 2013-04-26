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

    def test_techno_base(self):
        """update features of techno"""
        tech = Techno.objects.create(name="TechTestU1", public=1, cost_ore=2)
        self.assertEqual(tech.public, 1)
        self.assertEqual(tech.cost_ore, 2)
        self.assertEqual(tech.cost_research, 0)
