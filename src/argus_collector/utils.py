# coding=utf-8
"""Common utility functions shared for Python collectors"""

import errno
import json
import os
import pwd
import stat
import sys

from conf import settings


def err(msg):
    print >> sys.stderr, msg


def drop_privileges(user=settings.DROP_TO_USER):
    """Drops privileges if running as root."""
    try:
        ent = pwd.getpwnam(user)
    except KeyError:
        return

    # not root
    if os.getuid() != 0:
        return

    os.setgid(ent.pw_gid)
    os.setuid(ent.pw_uid)


def is_sockfile(path):
    """Returns whether or not the given path is a socket file."""
    try:
        s = os.stat(path)
    except OSError, (no, e):
        if no == errno.ENOENT:
            return False
        err("warning: couldn't stat(%r): %s" % (path, e))
        return None
    return s.st_mode & stat.S_IFSOCK == stat.S_IFSOCK


def is_numeric(value):
    return isinstance(value, (int, long, float))


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
        err(str(e))


def put_metric(host, port, _metric, _timestamp, _value, _tags):
    import requests

    api = '/api/put?details'
    url = 'http://{}:{}{}'.format(host, port, api)
    ret = requests.post(
        url=url,
        data=json.dumps(dict(
            metric=str(_metric),
            timestamp=int(_timestamp),
            value=str(_value),
            tags=dict(_tags)
        )))
    if ret.status_code != 200:
        raise Exception(str(ret.text))
    else:
        print_tsd(_metric, _timestamp, _value, **dict(_tags))
        # print 'put {} {} {} {}'.format(_metric, _timestamp, _value, _tags)


if __name__ == '__main__':
    print_tsd('aaa', 123, 100, a='1', b='2')
    # import socket
    # import time
    # import random
    #
    # host = '10.17.35.43'
    # port = 4242
    # addresses = socket.getaddrinfo(host, port,
    #                                socket.AF_UNSPEC,
    #                                socket.SOCK_STREAM, 0)
    # print addresses
    # for family, socktype, proto, canonname, sockaddr in addresses:
    #     try:
    #         tsd = socket.socket(family, socktype, proto)
    #         tsd.settimeout(15)
    #         tsd.connect(sockaddr)
    #         print 'Connected!'
    #         ct = int(time.time())
    #         a_year_ago = ct - 366 * 24 * 60 * 60
    #         tsd_metrics = ''
    #         for t in range(a_year_ago, ct, 3600):
    #             tsd_metrics += 'put {m} {t} {v} author=eacon\n'.format(
    #                 m='TAIHE.ETL_TRMNL_KQI_WEB.m.hour.fileCount',
    #                 t=t,
    #                 v=100 + random.randint(1, 100)
    #             )
    #         print tsd_metrics
    #         tsd.sendall(tsd_metrics)
    #         print 'Sent!'
    #     except:
    #         pass

    # ct = int(time.time())
    # for i, _time in enumerate(range(ct, ct - 3600 * 24 * 30, -3600 * 24)):
    #     put_metric(
    #                 host='10.17.35.43',
    #                 port=4242,
    #                 _metric='TAIHE.ETL_TRMNL_KQI_WEB.m.recordCount',
    #                 _timestamp=_time,
    #                 _value=100 + i,
    #                 _tags={'host': 'eacon_mac'}
    #             )
    # for _ in xrange(4000):
    #     for tag_type in ('WF_T_SERV_INFO_D', 'WF_T_SERV_INFO', 'WF_T_SERV_HIST_D', 'WF_T_SERV_HIST'):
    #         put_metric(
    #             host='10.17.35.43',
    #             port=4242,
    #             _metric='TAIHE.ETL_SERV_INFO_HIST.m.hour.fileCount',
    #             _timestamp=ct + _,
    #             _value=_ % 100,
    #             _tags={'type': tag_type}
    #         )
    #         put_metric(
    #             host='10.17.35.43',
    #             port=4242,
    #             _metric='TAIHE.ETL_SERV_INFO_HIST.m.hour.fileSize',
    #             _timestamp=int(time.time()),
    #             _value=_ % 100 + 1024,
    #             _tags={'type': tag_type}
    #         )