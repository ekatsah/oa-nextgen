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
from stock.models import Player, Techno, Scheme
from command import Command


class Subscribe(Command):
    name = models.CharField(max_length=40);

    def resolv(self):
        neutral = Player.objects.get(name="Void")
        if neutral.assets.count() == 0:
            raise Exception("Not enough neutral assets")

        player = Player.objects.create(name=self.name, is_active=True, 
                                       is_admin=False)

        # let's give him a solar system
        new_asset = neutral.assets.all()[0]
        new_asset.owner = player
        new_asset.save()

        # also, all the public technology
        for techno in Techno.get_publics():
            player.technos.add(techno)

        # also, all the public scheme
        for scheme in Scheme.get_publics():
            player.schemes.add(scheme)

    def __str__(self):
        args = (Command.__str__(self), self.name)
        return "Subscribe: base(%s), name = '%s'" % args


class SubscribeView(CreateView):
    model = Subscribe
    template_name = 'subscribe.html'
    success_url = '/'