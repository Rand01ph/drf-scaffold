#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------------------------------------------
#  FileName    :    models.py
#  Author      :    Rand01ph@
#  Project     :    drf_project/core
#  Date        :    2016-10-31
#  Description :    db models
# -----------------------------------------------------

from django.db import models

class Example(models.Model):

    content = models.CharField(max_length=100)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'example'

    def __unicode__(self):
        return u'id: <%d>' % self.pk
