# -*- coding: utf-8 -*-
#
# Copyright 2013, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.conf.urls import patterns, include, url
from django.views.generic.detail import DetailView
from law.general import SubscribeView
from stock.models import Player

urlpatterns = patterns('',
    url(r'^realm/(?P<pk>\d+)/$', 
        DetailView.as_view(queryset=Player.objects.all(),
                           template_name="realm.html"),
        name='realm'),

    url(r'^subscribe/$',
        SubscribeView.as_view(),
        name='subscribe'),
)
