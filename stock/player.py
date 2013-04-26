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
    technos = models.ManyToManyField("Techno", related_name="owners")
    schemes = models.ManyToManyField("Scheme", related_name="possessors")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'name'
