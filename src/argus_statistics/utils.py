#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Some utilities for extsvr package"""
from urllib import request
from urllib import parse
import json
import logging

import redis
from pymongo import MongoClient
from argus_statistics.settings import *

# MONGO_DB_HOST = '10.17.35.43'
# MONGO_DB_HOST = '192.168.0.253'
# MONGO_DB_PORT = 27017
# OPENTSDB_HOST = '10.17.35.43'
# OPENTSDB_HOST = "192.168.0.253"
# OPENTSDB_PORT = 4242


def get_client():
    """Return a mongodb client"""

    try:
        client = MongoClient(host=MONGO_DB_HOST, port=MONGO_DB_PORT)
    except Exception as e:
        raise
    return client

def get__mongo_cursor(dbname,collection_name):
    mongo_client = get_client()
    if collection_name == "":
        return 0
    else:
        db = mongo_client[dbname]
        col_cursor = db[collection_name]
        return col_cursor


def get_redis(redis_server:str, redis_port:int, db=0):
    redis_client = redis.StrictRedis(host=redis_server, port=redis_port, db=db)
    return redis_client

def urlopen(base_url: str, param: dict=dict()):
    """A url handler for update process which use opentsdb api with http GET verb."""

    try:
        query_param = parse.urlencode(param)
        url = base_url + query_param
        response = request.urlopen(url,timeout=5)
    except Exception as e:
        raise
    return response


def send_to_db(dbname, collection, data):
    try:
        client = MongoClient(host=MONGO_DB_HOST, port=MONGO_DB_PORT)
    except Exception as e:
        raise
    db = client[dbname]
    collection = db[collection]
    collection.insert_one(data)


def update_to_db(single_filter,dbname, collection, data):
    try:
        client = MongoClient(host=MONGO_DB_HOST, port=MONGO_DB_PORT)
    except Exception as e:
        raise
    db = client[dbname]
    collection = db[collection]
    collection.update_one(single_filter, data)



def check_tsdb():
    """Whether or not the OPENTDSDB is alive."""

    url = f'http://{OPENTSDB_HOST}:{OPENTSDB_PORT}/api/version'
    try:
        urlopen(url)
    except Exception as e:
        return False
    else:
        return True


def check_scale(metric: str, interval_time: str):
    r"""Try to make sure the last time series are valuable.

    :param metric: Metric name to be check out in OPENTSDB.
    :return: (int, []) represent the current valid cluster scale and ignored tags(dict) list responsively
    :rtype: tuple Object with 2 elements, int and list
    """

    cluster = Cluster('argus-statistics', 'scale', 'test')
    count = 0
    ignored = []

    for i in range(2):
        param = {
                'start': f'{interval_time}-ago',
                'm': f'count:{metric}' + '{host=*}',
        }
        response = urlopen(f'http://{OPENTSDB_HOST}:{OPENTSDB_PORT}/api/query?', param)
        if response.status == 200:
            raw = json.load(response)
        else:
            continue
        for ii in raw:
            # print(f'{i+1}/2', ii)
            if ii['dps']:
                    count += 1
            else:
                ignored.append(ii['tags'])
        if i == 1:  # last try
            break

        if count != cluster.scale:
            count = 0
            ignored.clear()
            continue

    return (count, ignored)


class Cluster(object):
    """A class refer to cluster configuration."""

    def __init__(self, db_name: str, scale_coll_name: str, weight_coll_name: str):  # TODO singleton???
        self._db_name = db_name
        self._scale_coll_name = scale_coll_name
        self._weight_coll_name = weight_coll_name

    @property
    def scale(self):
        client = get_client()
        db = client[self._db_name]
        coll = db[self._scale_coll_name]
        result = coll.find()

        return result[0]['count']

    @scale.setter
    def scale(self, new_count):
        client = get_client()
        db = client[self._db_name]
        coll = db[self._scale_coll_name]
        coll.update_one({'name': self._scale_coll_name}, {'$set': {'count': new_count}})
        print(coll)

        return self.scale

    @property
    def metric_weight(self):  # TODO finish metric and weight setting
        client = get_client()
        db = client[self._db_name]
        coll = db[self._weight_coll_name]
        cursor = coll.find()
        result = []
        for c in cursor:
            result.append(c)

        return result


if __name__ == '__main__':
    pass
    # send_to_db("argus-statistics", "sys_resource", data)
