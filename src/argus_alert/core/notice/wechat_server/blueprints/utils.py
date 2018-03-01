#!/usr/bin/env python
# -*- coding: utf-8 -*-

from logging.handlers import TimedRotatingFileHandler
import logging
import functools
import os
import time

import requests

__all__ = ['get_access_token', 'get_app_token', 'get_logger', 'singleton']

app_id = os.environ.get('WECHAT_APPID') or 'wxf3ec4b681e848199',
secret = os.environ.get('WECHAT_SECRET') or '61aa0e8881296ca0514fd1f5aaac02be'


def _cache_access_token(f):
    """A access_token cache decorator for wechat policy."""

    _last_token = {}

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        nonlocal _last_token
        current = int(time.time())
        check_time = int(_last_token.get('check_time') or current)
        expires_in = int(_last_token.get('expires_in') or -1)
        deadline = check_time + expires_in
        is_expired = True if deadline <= current else False
        if is_expired:
            _last_token = f(*args, **kwargs)  # a new object new memory address
            _last_token['check_time'] = current
        return _last_token['access_token']
    return wrapper


def _cache_access_token_v2(f):
    """A access_token cache decorator for wechat policy."""

    _last_token = {}

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        current = int(time.time())
        check_time = int(_last_token.get('check_time') or current)
        expires_in = int(_last_token.get('expires_in') or -1)
        deadline = check_time + expires_in
        is_expired = True if deadline <= current else False
        if is_expired:
            print('It is expired, so getting a new token.')
            result = f(*args, **kwargs)

            _last_token['access_token'] = result['access_token']
            _last_token['expires_in'] = result['expires_in']
            _last_token['check_time'] = current
        else:
            print('It is not expired, so return a old token.')
        return _last_token['access_token']
    return wrapper


@_cache_access_token_v2
def get_access_token():
    url = 'https://api.weixin.qq.com/cgi-bin/token'
    params = {'grant_type': 'client_credential',
              'appid': app_id,
              'secret': secret}
    r = requests.get(url=url, params=params)
    result = r.json()
    print(f'Raw result of getting access token:\n {result}')
    return result


def singleton(cls):
    """A singleto decorator."""

    _instance = {}

    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        key = f'<{cls}> object <{args}> <kwargs>'
        if key not in _instance.keys():
            _instance[key] = cls(*args, **kwargs)
        return _instance[key]
    return get_instance


def get_app_token():
    return os.environ.get('WECHAT_APP_TOKEN') or 'random_token'


def get_logger(file_name, level=logging.INFO, when='d', interval=1, backupCount=7):
    base_path = os.path.abspath(os.path.dirname(__file__))
    logger = logging.getLogger(file_name)
    logger.setLevel(level)
    log_path = os.path.join(base_path, 'data/', file_name)
    fh = TimedRotatingFileHandler(filename=log_path, when=when, interval=interval,
                                  backupCount=7)
    fh.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
