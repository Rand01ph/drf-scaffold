#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------------------------------------------
#  FileName    :    views.py
#  Author      :    Rand01ph@
#  Project     :    drf_project/example
#  Date        :    2016-10-31
#  Description :    views
# -----------------------------------------------------

import logging

from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework import generics, mixins

from core.models import Example

from utils.response import NormalResponse
from .serializers import ExampleSerializer

logger = logging.getLogger(__name__)

class ExampleView(mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  generics.GenericAPIView):

    """
    example:
    """

    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)
    parser_classes = (JSONParser,)
    queryset = Example.objects.all()
    lookup_url_kwarg = ('event_id')
    lookup_field = ('event_id')
    serializer_class = ExampleSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return NormalResponse(result=serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return NormalResponse(result=ExampleSerializer(serializer.instance).data)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return NormalResponse(result=ExampleSerializer(serializer.instance).data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return NormalResponse(result='')
