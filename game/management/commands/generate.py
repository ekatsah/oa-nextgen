# -*- coding: utf-8 -*-
#
# Copyright 2013, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from random import randint
from django.core.management.base import BaseCommand, CommandError
from game.config import *
from game.utils import randname
import stock.models as models


class Command(BaseCommand):
    help = """Fill a DB with things"""

    def handle(self, *args, **options):

        # Weapons generation
        print "weapons generation"
        W = models.Weapon.objects.create
        laser1 = W(name="Laser I", spa_attack=1, shield_attack=1, velocity=10,
                   scope=5, accuracy="20,15,10,5,0,0,0,0,0,0")
        
        bomb1 = W(name="Bombe I", pla_attack=3, velocity=5, scope=10,
                  accuracy="0,0,0,0,0,0,0,0,0,0")

        # Technos generation
        print "technos generation"
        T = models.Techno.objects.create
        mine1 = T(name="Mine I", extract=1, type="building", cost_prod=10, 
                  cost_ore=1, structural=10, public=1)

        mine2 = T(name="Mine II", parent=mine1, extract=2, type="building", 
                  cost_prod=20, cost_ore=1, structural=15, cost_research=100)

        rea1 = T(name="Reactor I", propeller=1, type="component",
                 cost_prod=2, cost_ore=1, structural=1, public=True)

        shield1 = T(name="Shield I", shield=1, type="component",
                    cost_prod=5, cost_ore=1, structural=1, public=True)

        cargo1 = T(name="Cargo I", cargo=10, type="component",
                   cost_prod=2, cost_ore=2, structural=2, parent=rea1,
                   cost_research=100,)

        scan1 = T(name="Scanner I", syst_scan=1, type="component",
                  cost_prod=10, cost_ore=5, structural=1, parent=rea1,
                  cost_research=140)

        las1 = T(name="Laser I", parent=rea1, weapon=laser1, type="component",
                 cost_prod=2, cost_ore=2, structural=1, cost_research=100,
                 militarian=True)

        bom1 = T(name="Bomb I", parent=las1, weapon=bomb1, type="component",
                 cost_prod=5, cost_ore=2, structural=1, cost_research=200,
                 militarian=True)

        # Neutral player generation
        print "neutral player generation"
        neutral = models.Player.objects.create(name="Void")

        # Scheme generation
        print "schemes generation"
        S = models.Scheme.objects.create
        cargo = S(name="Minor Fret", brand="GalactaCorp", domain="public",
                  owner=neutral)
        cargo.add_compo(rea1, 1)
        cargo.add_compo(cargo1, 2)
        cargo.finalize()

        fighter = S(name="Minor Fighter", brand="GalactaCorp", domain="public",
                    owner=neutral)
        fighter.add_compo(rea1, 1)
        fighter.add_compo(shield1, 1)
        fighter.add_compo(las1, 2)
        fighter.finalize()

        bomber = S(name="Minor Bomber", brand="GalactaCorp", domain="public",
                   owner=neutral)
        bomber.add_compo(rea1, 1)
        bomber.add_compo(shield1, 1)
        bomber.add_compo(bom1, 5)
        bomber.finalize()

        # Systems generation
        print "systems generation"
        for _ in xrange(SYSTEM_QUANTITY):
            x, y = 0, 0
            while models.System.objects.filter(x=x, y=y).count() > 0:
                x = randint(-GALAXY_BOUND, GALAXY_BOUND)
                y = randint(-GALAXY_BOUND, GALAXY_BOUND)
            models.System.objects.create(x=x, y=y)

        # Assets generation
        print "assets generation"
        for system in models.System.objects.all():
            models.Asset.objects.create(system=system, name=randname(), 
                                        owner=neutral)

        # Planets generation
        print "planets generation"
        P = models.Planet.objects.create
        for asset in models.Asset.objects.all():
            planet_count = randint(PLANET_MIN, PLANET_MAX)
            for position in map(lambda p: p + 1, xrange(planet_count)):
                size = randint(1, 4)
                P(system=asset.system, asset=asset, position=position, 
                  temperature=randint(0, 100), radiation=randint(0, 100),
                  structure=size * 20 + randint(0, 30), taxe=2, stability=100,
                  ore=randint(0, 6), size=size)
