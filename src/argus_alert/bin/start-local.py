#!/usr/bin/env python3
# coding=utf-8
"""本地模式启动
"""
import sys
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(base_dir))

from argus_alert.bin import manage
from argus_alert.core.utils.common import daemonize
from argus_alert.core.utils.log import timed_logger


def main():
    daemonize()
    LOG = timed_logger()
    sys.argv = ['manage.py',
                '--start-driver',
                '--start-executor', '--executor-worker', '1',
                '--start-notifier', '--notifier-worker', '1',
                ]

    try:
        manage.main()
    except Exception as e:
        LOG.error(e, exc_info=True)


if __name__ == '__main__':
    main()
