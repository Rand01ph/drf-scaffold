#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------------------------------------------
#  FileName    :    serializers.py
#  Author      :    tanyawei@
#  Project     :    hato/event
#  Date        :    2016-04-21
#  Description :    serializers
# -----------------------------------------------------

from rest_framework import serializers

from core.models import Example

class ExampleSerializer(serializers.Serializer):

    content = serializers.CharField()
    update_time = serializers.DateTimeField(required=False)
    create_time = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        return Example.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance
