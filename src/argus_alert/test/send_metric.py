# coding=utf-8
"""
"""
from __future__ import division
import json
import socket
import time
import random

import requests


def print_tsd(metric, timestamp, value, **tags):
    """
    print a formatted time-series-data:
     put {metric} {timestamp} {value} {tags_string}
    """
    try:
        if not tags:
            raise Exception('No tags for a tsd!\n\t{} {} {}\n'.format(metric, timestamp, value))
        tags_str = ' '.join('{}={}'.format(k, v) for k, v in tags.iteritems())
        print('put {metric} {timestamp} {value} {tags}'.format(
            metric=metric,
            timestamp=timestamp,
            value=value,
            tags=tags_str,
        ))
    except Exception as e:
        print(str(e))


def update_metric(host, port, _metric, _timestamp, _value, _tags, method='post'):
    api = '/api/put?details'
    url = 'http://{}:{}{}'.format(host, port, api)
    if method == 'post':
        data = json.dumps(dict(
            metric=str(_metric),
            timestamp=int(_timestamp),
            value=str(_value),
            tags=dict(_tags)))
    elif method == 'delete':
        data = json.dumps(dict(
            metric=str(_metric),
            timestamp=int(_timestamp),
            # value=str(_value),
            tags=dict(_tags)))
    else:
        data = {}
    ret = requests.request(method=method, url=url, data=data)
    if ret.status_code != 200:
        raise Exception(str(ret.text))
    else:
        print_tsd(_metric, _timestamp, _value, **dict(_tags))
        # print 'put {} {} {} {}'.format(_metric, _timestamp, _value, _tags)


if __name__ == '__main__':
    pass

    # update_metric(
    #     method='delete',
    #     host='132.122.70.138',
    #     port=4242,
    #     _metric='TAIHE.ETL_4G_MRO_ERS.m.day.recordCount',
    #     _timestamp=1505750399,
    #     _value=720014333,
    #     _tags={'host': 'TH04-ZNWG-SGI620-040'}
    # )


    host = 'localhost'
    # host = '10.17.35.43'
    port = 4242
    addresses = socket.getaddrinfo(host, port,
                                   socket.AF_UNSPEC,
                                   socket.SOCK_STREAM, 0)
    for family, socktype, proto, canonname, sockaddr in addresses:
        try:
            tsd = socket.socket(family, socktype, proto)
            tsd.settimeout(15)
            tsd.connect(sockaddr)
            print(f'Connected {sockaddr}!')
            ct = int(time.time())
            a_year_ago = ct - 366 * 24 * 60 * 60
            a_month_ago = ct - 31 * 24 * 60 * 60
            a_hour_ago = ct - 60 * 60
            _7h_ago = ct - 60 * 60 * 7
            metric_values = [
                ('sys.cpu.usage', lambda :format(float(random.random()), '0.2f')),
                # ('sys.network.lossrate', lambda :format(float(random.random()), '0.2f')),
                ('sys.disk.usage', lambda :format(float(random.random()), '0.2f')),
                # ('hdfs.disk.usage', lambda :format(float(random.random()), '0.2f')),
                # ('hbase.disk.used', lambda : random.random() * 4096 * 1024 * 1024),
                # ('hadoop.job.time', lambda : random.choice([100, 300, 200, 400, 500])),
                # ('spark.job.time', lambda : random.choice([100, 300, 200, 400, 500])),
                # ('TAIHE.ETL_4G_MRO_ERS.m.hour.fileCount', lambda :random.choice([10000, 20000, 30000])),
                # ('TAIHE.ETL_4G_MRO_ERS.m.hour.fileCount', lambda :random.choice([240000, 250000, 260000])),


            ]

            # tsd_metrics = ''


            # for m, _v in metric_values:
            #     for t in range(a_hour_ago, ct, 5):
            #         v = _v()
            #         tsd_metrics += f'put {m} {t} {v} host=EaconMBP\n'
            #     tsd.sendall(bytes(tsd_metrics, encoding='utf-8'))
            #     print(tsd_metrics[:80])
            #

            # put sys.disk.usage

            while True:
                for n in (range(1, 11)):
                    v = n/10
                    m = 'sys.disk.usage'
                    t = int(time.time())
                    print(f'value: {v}')
                    tsd_metrics = f'put {m} {t} {v} host=EaconMBP\n'
                    tsd.sendall(bytes(tsd_metrics, encoding='utf-8'))
                    print('sent...')
                    time.sleep(20)

            print('All sent!')
        except Exception as e:
            print(e)
            pass
        else:
            break
