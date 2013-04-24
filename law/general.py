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
from command import Command
from stock.models import Player

class Subscribe(Command):
    name = models.CharField(max_length=40);

    def resolv(self):
        Player.objects.create(name=self.name, is_active=True, is_admin=False)

    def __str__(self):
        args = (Command.__str__(self), self.name)
        return "Subscribe: base(%s), name = '%s'" % args

class SubscribeView(CreateView):
    model = Subscribe
    template_name = 'subscribe.html'
    success_url = '/'