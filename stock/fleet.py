# -*- coding: utf-8 -*-
#
# Copyright 2013, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.db import models
from game.config import GALAXY_BOUND
from game.feature import FeatureFactory
from game.utils import poc2size
from player import Player
from scheme import Scheme


class FleetShips(models.Model):
    fleet = models.ForeignKey("Fleet")
    scheme = models.ForeignKey(Scheme)
    race = models.CharField(max_length=40)
    number = models.IntegerField()
    damage = models.IntegerField(default=0)


class Fleet(models.Model):
    owner = models.ForeignKey(Player, related_name="fleets")
    name = models.CharField(max_length=40)
    pos_x = models.IntegerField(default=GALAXY_BOUND + 10)
    pos_y = models.IntegerField(default=GALAXY_BOUND + 10)
    dest_x = models.IntegerField(default=GALAXY_BOUND + 10)
    dest_y = models.IntegerField(default=GALAXY_BOUND + 10)

    # Features
    militarian = models.BooleanField(default=False)
    cargo_capacity = models.IntegerField(default=0)
    behaviour = models.CharField(max_length=40, default="neutral")
    target = models.IntegerField(default=0)
    spa_attack = models.IntegerField(default=0)
    pla_attack = models.IntegerField(default=0)
    velocity = models.IntegerField(default=-1)
    syst_scan = models.IntegerField(default=0)
    fleet_scan = models.IntegerField(default=0)
    build_order = models.ForeignKey(Scheme, default=None, null=True, related_name="built_by")
    size = models.CharField(max_length=40)
    damage = models.IntegerField(default=0)

    features = FeatureFactory("militarian", "cargo_capacity", "behaviour",
                              "spa_attack", "pla_attack", "velocity",
                              "syst_scan", "fleet_scan", "size", "damage")

    def ships(self):
        return FleetShips.objects.filter(fleet=self)

    def add_ships(self, scheme, race, number, damage=0):
        query = self.ships().filter(scheme=scheme, race=race)
        if query.count() > 0:
            fleetship = query[0]
            fleetship.number += number
            fleetship.damage += damage
            fleetship.save()
        else:
            FleetShips.objects.create(fleet=self, scheme=scheme, race=race, 
                                      number=number, damage=damage)

    def finalize(self):
        self.cargo_capacity, self.militarian, self.spa_attack = 0, False, 0
        self.pla_attack, self.velocity, self.syst_scan = 0, 100, 0
        self.fleet_scan, fleet_damage, poc = 0, 0, 0

        query = self.ships().values_list("scheme", "number", "damage")
        for ship, number, damage in query:
            ship = Scheme.objects.get(id=ship)

            if ship.militarian == True:
                self.militarian = True

            self.cargo_capacity += ship.cargo * number
            self.spa_attack += ship.spa_attack * number
            self.pla_attack += ship.pla_attack * number
            self.syst_scan = max(self.syst_scan, ship.syst_scan)
            self.fleet_scan = max(self.fleet_scan, ship.fleet_scan)
            self.velocity = min(self.velocity, ship.velocity)
            poc += ship.poc * number
            fleet_damage += damage

        self.damage = fleet_damage * 200 / poc
        self.size = "fsize" + str(poc2size(poc, self.spa_attack,
                                           self.pla_attack))
        self.save()
