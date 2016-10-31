
#! /usr/bin/env python
# coding=utf-8
# author: Rand01ph

import logging

from django.http import JsonResponse
from django.db import IntegrityError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.compat import set_rollback
from rest_framework.exceptions import ParseError
from rest_framework.serializers import ValidationError

logger = logging.getLogger('drf_project.errors')

class Error(Exception):

    def __init__(self, err_code, err_result='Internal Server Error',
                 message=u'Server Error', status_code=status.HTTP_200_OK):
        self.err_code = err_code
        self.err_result = err_result
        self.message = message
        self.status_code = status_code

    def __unicode__(self):
        return u'[Error] %d: %s(%d)' % (self.err_code, self.err_result, self.status_code)

    def getResponse(self):
        return ErrorResponse(self.err_code, self.err_result, self.message, self.status_code)


def ErrorResponse(err_code=1000, err_result='Nuknow Error',
                  message=u'unknow error', status=status.HTTP_200_OK, headers=None):
    err = {
        'status': err_code,
        'module': 'drf_project',
        'message': message,
        'result': err_result,
    }
    return Response(err, status, headers=headers)

# custom error
class CustomtabNameBlankError(Error):
    def __init__(self):
        super(CustomtabNameBlankError, self).__init__(err_code=2101,
                                               message=u'Please make sure customtab name is not blank')

def custom_exception_handler(exc, context):

    if isinstance(exc, Error):
        set_rollback()
        logger.error(exc)
        return ErrorResponse(exc.err_code, exc.err_result, exc.message, status=exc.status_code)

    if isinstance(exc, KeyError):
        data = 'key error.'
        set_rollback()
        logger.error(exc)
        return ErrorResponse(2001, data, u'KeyError', status=status.HTTP_200_OK)

    if isinstance(exc, ParseError):
        data = exc.detail
        set_rollback()
        logger.error(exc)
        return ErrorResponse(2001, data, u'parse error', status=status.HTTP_200_OK)

    if isinstance(exc, ValidationError):
        data = exc.detail
        if data.has_key('email_title'):
            return ErrorResponse(2104, data, u'email_title can not be null', status=status.HTTP_200_OK)
        set_rollback()
        logger.error(exc)
        return ErrorResponse(2001, data, u'validation error', status=status.HTTP_200_OK)

    if isinstance(exc, IntegrityError):
        data = str(exc)
        return ErrorResponse(3101, data, u'duplicate error', status=status.HTTP_200_OK)
    # Note: Unhandled exceptions will raise a 500 error.
    # return ErrorResponse(errors.SYSTEM_ERROR, 'Internal Server Error', status.HTTP_500_INTERNAL_SERVER_ERROR)

def render_404(request):
    err = {
        'status': 2000,
        'module': 'drf_project',
        'message': 'success',
        'result': {},
    }
    logger.error(request)
    return JsonResponse(err, status=status.HTTP_200_OK)

def render_500(request):
    err = {
        'status': 1001,
        'module': 'drf_project',
        'message': 'Internal Server Error',
        'result': {},
    }
    logger.error(request)
    return JsonResponse(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
