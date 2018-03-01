#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This python file is used to fetch all metrics in OPENTSDB
"""

import json
import urllib2
import time
import threading 

from argus_collector.web.data.settings import OPEN_TSDB_HOST, OPEN_TSDB_PORT


def get_metrics():
    """
    http :{port}/api/suggest?type=metrics&max=???

    returntype dict containing all the metric names in OPENTSDB
    """
    host = OPEN_TSDB_HOST
    port = OPEN_TSDB_PORT

    _url = 'http://{0}:{1}/api/stats'.format(host, port)
    raw_response = urllib2.urlopen(_url)
    meta_data = json.loads(raw_response.read())
    quantity = 9
    for item in meta_data:
        if item['metric'] == 'tsd.uid.ids-used':
            quantity += int(item['value'])
    
    url = 'http://{0}:{1}/api/suggest?type=metrics&max={2}'.format(host, port, quantity)
    raw_response = urllib2.urlopen(url)
    metrics = json.load(raw_response)
    return metrics


def get_last_data_points(metrics_dict, container):
    """
    Get each metric's last data points via a single api request.
    http :{port}/api/query/last?timeseries={metric_name{tag1, tag2, ...}}
    """

    host = OPEN_TSDB_HOST
    port = OPEN_TSDB_PORT
    # for metric in metrics_dict:
        # _url = 'http://{0}:{1}/api/query/last?timeseries={2}'.format(host, port, metric)
        # raw_response = urllib2.urlopen(_url)
        ## a list comprise of dicts
        # data_points = json.loads(raw_response.read())
        # last = - 1
        # if not data_points:
            # container.append((metric, -1))
            # continue
        # for i in data_points:
            # if i['timestamp'] > last:
                # last = i['timestamp']
        # container.append((metric, last))

    for metric in metrics_dict:
        _url = 'http://{0}:{1}/api/query?start=30m-ago&m=sum:{2}{}'.format(host, port, metric)

        # simple output:
        # [
            # {
                # "aggregateTags": [
                    # "host"
                # ],
                # "dps": {
                    # "1508490100": 0.25999999915560085,
                    # "1508490200": 0.20999999965230623,
                    # "1508491800": 0.3499999977648258
                # },
                # "metric": "cluster.cpu.usage",
                # "tags": {}
            # }
        # ]

        raw_response = urllib2.urlopen(_url)
        try:
            data_points = json.load(raw_response)[0]['dps']
        except Exception as e:
            print(metric, 'is not available')
            data_points = None
        if not data_points:
            container.append((metric, -2))
            continue
        last = max(map(int, data_points.keys()))
        container.append((metric, last))


if __name__ == '__main__':
    get_metrics()
