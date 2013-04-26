# -*- coding: utf-8 -*-
#
# Copyright 2013, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.core.management.base import BaseCommand, CommandError
from stock.models import Scheme


class Command(BaseCommand):
    help = """Resolv a week"""

    def handle(self, *args, **options):
        for scheme in Scheme.objects.all():
            scheme.finalize()
