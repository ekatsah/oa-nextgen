# -*- coding: utf-8 -*-
#
# Copyright 2013, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

import models
from django.shortcuts import render
from django.db.models.base import ModelBase
from django.views.generic.edit import CreateView
from command import Command

class OrderView(CreateView):
    template_name = 'order.html'
    success_url = '/order/'


def all_order(request):
    orders = [ name for name in models.__dict__
               if isinstance(getattr(models, name), ModelBase) ] 
    return render(request, "order_list.html", {"orders": orders})


def one_order(request, name):
    order = getattr(models, name)

    class View(CreateView):
        template_name = 'order.html'
        success_url = '/order/'
        model = order

    return (View.as_view())(request)


def orders_list(request):
    orders = [ getattr(models, name) for name in models.__dict__
               if isinstance(getattr(models, name), ModelBase) ]

    stop, week, orders_list = False, 0, {}
    while not stop:
        stop = True

        orders_list[week] = []
        for order in orders:
            cmds = order.objects.filter(week=week)
            orders_list[week].append(cmds)
            if len(cmds) > 0:
                cmds = False

        week += 1
    return render(request, "orders_list.html", {"orders": orders_list})