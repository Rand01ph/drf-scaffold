#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Rand01ph on 2019/5/6


from django.utils import timezone
from rest_framework import serializers


class DateTimeFieldWihTZ(serializers.DateTimeField):

    def to_representation(self, value):
        value = timezone.localtime(value)
        return super(DateTimeFieldWihTZ, self).to_representation(value)
