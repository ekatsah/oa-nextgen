# -*- coding: utf-8 -*-
#
# Copyright 2013, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.core.management.base import BaseCommand, CommandError
import stock.models as models

class Command(BaseCommand):
    help = """Fill a DB with things"""

    def handle(self, *args, **options):
        models.System.generate()
        models.Asset.generate()
        models.Planet.generate()
