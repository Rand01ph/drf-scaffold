#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------------------------------------------
#  FileName    :    urls.py
#  Author      :    Rand01ph@
#  Project     :    drf_project/example
#  Date        :    2016-10-31
#  Description :    urls
# -----------------------------------------------------

from django.conf.urls import url
from . import views

urlpatterns = (
    url(r'^$', views.ExampleView.as_view()),
)
