# -*- coding: utf-8 -*-
#
# Copyright 2013, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.core.management.base import BaseCommand, CommandError
import law.models as models


class Command(BaseCommand):
    help = """Resolv a week"""

    def handle(self, *args, **options):
        for order_type in ["Subscribe"]:
            for order in getattr(models, order_type).objects.all():
                print str(order)
                order.resolv()
