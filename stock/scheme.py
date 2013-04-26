# -*- coding: utf-8 -*-
#
# Copyright 2013, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.db import models
from game.feature import FeatureFactory
from game.utils import struct2size
from player import Player
from techno import Techno


class SchemeCompo(models.Model):
    scheme = models.ForeignKey("Scheme")
    techno = models.ForeignKey(Techno)
    number = models.IntegerField()


class SchemeMerch(models.Model):
    scheme = models.ForeignKey("Scheme")
    merch = models.CharField(max_length=40)
    amount = models.IntegerField(default=1)


class Scheme(models.Model):
    owner = models.ForeignKey(Player, related_name="created")
    name = models.CharField(max_length=40)
    brand = models.CharField(max_length=40)
    domain = models.CharField(max_length=40)

    # Features
    militarian = models.BooleanField(default=False)
    size = models.IntegerField(default=0)
    poc = models.IntegerField(default=0)
    velocity = models.IntegerField(default=-1)
    cost_prod = models.IntegerField(default=0)
    cost_ore = models.IntegerField(default=0)
    cargo = models.IntegerField(default=0)
    syst_scan = models.IntegerField(default=0)
    fleet_scan = models.IntegerField(default=0)
    scm = models.IntegerField(default=0)
    colo = models.BooleanField(default=False)
    spa_attack = models.IntegerField(default=0)
    pla_attack = models.IntegerField(default=0)
    shield = models.IntegerField(default=0)

    features = FeatureFactory("size", "poc", "velocity", "spa_attack",
                              "pla_attack", "syst_scan", "fleet_scan",
                              "cargo", "scm", "colo", "shield", "cost_prod", 
                              "cost_ore", "militarian")

    @staticmethod
    def get_publics():
        return Scheme.objects.filter(domain="public")

    def compos(self):
        return SchemeCompo.objects.filter(scheme=self)

    def add_compo(self, techno, number):
        query = self.compos().filter(techno=techno)
        if query.count() > 0:
            schemecompo = query[0]
            schemecompo.number += number
            schemecompo.save()
        else:
            SchemeCompo.objects.create(scheme=self, techno=techno,
                                       number=number)

    def finalize(self):
        structure, engine = 0, 0
        self.cargo, self.militarian, self.cost_prod = 0, False, 0
        self.cost_ore, self.syst_scan, self.fleet_scan = 0, 0, 0
        self.colo, self.spa_attack, self.pla_attack = False, 0, 0
        self.shield, self.scm = 0, 0

        for tech, number in self.compos().values_list("techno", "number"):
            tech = Techno.objects.get(id=tech)

            if tech.militarian == True:
                self.militarian = True

            if tech.colo == True:
                self.colo = True

            self.cargo += tech.cargo * number
            self.cost_prod += tech.cost_prod * number
            self.cost_ore += tech.cost_ore * number
            self.shield += tech.shield * number
            self.syst_scan = max(self.syst_scan, tech.syst_scan)
            self.fleet_scan = max(self.fleet_scan, tech.fleet_scan)
            self.scm = max(self.scm, tech.scm)
            if tech.weapon:
                self.spa_attack += tech.weapon.spa_attack * number
                self.spa_attack += tech.weapon.shield_attack * number
                self.pla_attack += tech.weapon.pla_attack * number
            structure += tech.structural * number
            engine = max(engine, tech.propeller)

        self.size = struct2size(structure)
        self.poc = max(1, int(structure / 2))
        self.velocity = 12 - self.size + engine
        self.save()
