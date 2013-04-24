# -*- coding: utf-8 -*-
#
# Copyright 2013, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.db import models
from game.feature import Feature


class TechnoFeature(models.Model):
    techno = models.ForeignKey('Techno')
    feature = models.ForeignKey(Feature)
    int_value = models.IntegerField(null=True)
    str_value = models.CharField(max_length=40)
    # 1 for int, 2 for code
    type = models.IntegerField(default=1)

    def value(self):
        if self.type == 1:
            return self.int_value
        else:
            return self.str_value


class Techno(models.Model):
    name = models.CharField(max_length=40, unique=True)
    features = models.ManyToManyField(Feature, through=TechnoFeature)
    parent = models.ForeignKey('self', null=True)

    @staticmethod
    def generate():
        mine1 = Techno.objects.create(name="Mine I")
        mine1.update_feature(extract=1, type="building", cost_prod=10,
                             cost_ore=1, structural=10, public=1)

        mine2 = Techno.objects.create(name="Mine 2", parent=mine1)
        mine2.update_feature(extract=2, type="building", cost_prod=20,
                             cost_ore=1, structural=15, cost_research=100)

    def update_feature(self, **kwargs):
        for code, value in kwargs.iteritems():
            feature = Feature.objects.get(code=code)
            if type(value) == int:
                TechnoFeature.objects.create(techno=self, feature=feature,
                                             int_value=value, type=1)
            else:
                referer = Feature.objects.get(code=value)
                TechnoFeature.objects.create(techno=self, feature=feature,
                                             str_value=code, type=2)

