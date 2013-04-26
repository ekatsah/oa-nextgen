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
from stock.models import Player, Techno, Scheme, Fleet
from command import Command


class Subscribe(Command):
    name = models.CharField(max_length=40)
    race = models.CharField(max_length=40)
    domain = models.CharField(max_length=40)

    def resolv(self):
        neutral = Player.objects.get(name="Void")
        if neutral.assets.count() == 0:
            raise Exception("Not enough neutral assets")

        P = Player.objects.create
        player = P(name=self.name, domain=self.domain, race=self.race,
                   started=self.week)

        # let's give him a solar system
        new_asset = neutral.assets.all()[0]
        new_asset.owner = player
        new_asset.save()

        # this first asset is the the facto capital of new player
        player.capital = new_asset
        player.save()

        # also, all the public technology
        for techno in Techno.get_publics():
            player.technos.add(techno)

        # also, all the public scheme
        for scheme in Scheme.get_publics():
            player.schemes.add(scheme)

        # make him a first fleet!
        starting_fleet = [("Minor Fret", 5), ("Minor Fighter", 10),
                          ("Minor Bomber", 12)]
        sys = new_asset.system
        F = Fleet.objects.create
        fleet = F(name="Starting Fleet", owner=player, pos_x=sys.x,
                  pos_y=sys.y, dest_x=sys.x, dest_y=sys.y)

        for scheme_name, number in starting_fleet:
            ship = Scheme.objects.get(name=scheme_name)
            fleet.add_ships(ship, self.race, number)
        fleet.finalize()

    def __str__(self):
        args = (Command.__str__(self), self.name)
        return "Subscribe: base(%s), name = '%s'" % args


class SubscribeView(CreateView):
    model = Subscribe
    template_name = 'subscribe.html'
    success_url = '/subscribe/'