#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------------------------------------------
#  FileName    :    urls.py
#  Author      :    Rand01ph@
#  Project     :    drf_project/core
#  Date        :    2016-10-31
#  Description :    urls
# -----------------------------------------------------

from django.conf.urls import include, url

urlpatterns = (
    url(r'^example/', include('example.urls')),
)
