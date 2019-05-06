#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Rand01ph on 18-8-27

import os
import yaml
import uuid

import redis
from watchman.decorators import check

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, 'config.yaml')) as conf_file:
    config = yaml.load(conf_file)

redis_cache_setting = config['cache']
REDIS_CACHE_HOST = redis_cache_setting['host']
REDIS_CACHE_PASSWORD = redis_cache_setting['password']
REDIS_CACHE_PORT = redis_cache_setting['port']
REDIS_CACHE_DB = redis_cache_setting['db']


def _check_caches(caches):
    return [_check_cache(cache) for cache in sorted(caches)]


@check
def _check_cache(cache_name):
    key = 'fanapi-django-watchman-{}'.format(uuid.uuid4())
    value = 'fanapi-django-watchman-{}'.format(uuid.uuid4())

    cache = redis.StrictRedis(host=REDIS_CACHE_HOST, port=REDIS_CACHE_PORT, db=REDIS_CACHE_DB,
                              password=REDIS_CACHE_PASSWORD)

    cache.set(key, value)
    cache.get(key)
    cache.delete(key)
    return {cache_name: {"ok": True}}


def caches():
    return {"caches": _check_caches(['pub_redis'])}
