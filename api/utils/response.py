#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------------------------------------------
#  FileName    :    response.py
#  Author      :    Rand01ph@
#  Project     :    drf_project/utils
#  Date        :    2016-10-31
# -----------------------------------------------------

from rest_framework import status
from rest_framework.response import Response

def NormalResponse(status_code=2000, result='',
                  message=u'success', status=status.HTTP_200_OK, headers=None):
    data = {
        'status': status_code,
        'module': 'drf_project',
        'message': message,
        'result': result,
    }
    return Response(data, status, headers=headers)
