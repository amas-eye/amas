#!/usr/bin/env python
# -*- coding: utf-8 -*-

from logging.handlers import TimedRotatingFileHandler
import logging
import urllib2
import json

from argus_collector.web.data.settings import OPEN_TSDB_HOST, OPEN_TSDB_PORT


def get_logger(file_name, level=logging.INFO, when='d', interval=1, backupCount=7):
    logger = logging.getLogger(file_name)
    logger.setLevel(logging.DEBUG)
    fh = TimedRotatingFileHandler(filename=file_name, when='D', interval=1,
                                  backupCount=7)
    fh.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


def get_tags(period, metric):
    """
    Add this method for Tapd Bug 1000013.
    http :{port}/api/query?start=5m-ago&m=sum:{metric_name}
    The following is 2 kinds of example output from origin OPENTSDB api.

    [
        {
            "aggregateTags": [
                "host"
            ],
            "dps": {
                "1508294900": 0.029999999329447746,
                "1508295000": 0.03999999910593033
            },
            "metric": "cluster.cpu.usage",
            "tags": {}
        }
    ]
    OR
    [
        {
            "aggregateTags": [],
            "dps": {
                "1508295023": 99,
                "1508295038": 99,
                },
            "metric": "test.hao.gpu",
            "tags": {
                "host": "localhost.localdomain"
            }
        }
    ]


    """
    host = OPEN_TSDB_HOST
    port = OPEN_TSDB_PORT

    _url = 'http://{0}:{1}/api/query?start={2}&m=sum:{3}'.format(host, port, period, metric)
    raw_response = urllib2.urlopen(_url)
    meta_data = json.load(raw_response)
    if not meta_data:  # no data
        return "There's  no data in this duration <%s>." % period
    inter_dict = meta_data[0]
    if inter_dict['aggregateTags']:  # ok
        return meta_data
    else:
        for k in inter_dict['tags']:
            inter_dict['aggregateTags'].append(k)
        return [inter_dict]
