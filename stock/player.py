# -*- coding: utf-8 -*-
#
# Copyright 2013, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.


from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class Player(AbstractBaseUser):
    name = models.CharField(max_length=40, unique=True, db_index=True)
    domain = models.CharField(max_length=40, default="Neutral Zone")
    race = models.CharField(max_length=40, default="mutant")
    started = models.IntegerField(default=0)
    alive = models.BooleanField(default=True)
    budget_tech = models.IntegerField(default=5)
    budget_spe = models.IntegerField(default=5)
    budget_cesp = models.IntegerField(default=5)
    capital_bank = models.IntegerField(default=20000)
    capital_tech = models.IntegerField(default=0)
    capital_spe = models.IntegerField(default=0)
    capital_cesp = models.IntegerField(default=0)
    technos = models.ManyToManyField("Techno", related_name="owners")
    schemes = models.ManyToManyField("Scheme", related_name="possessors")
    tmp_schemes = models.ManyToManyField("Scheme", related_name="tmpconst")
    capital = models.ForeignKey("Asset", related_name="capital_of", null=True)

    USERNAME_FIELD = 'name'
