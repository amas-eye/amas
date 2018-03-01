#!/usr/bin/python3
# coding=utf-8
"""告警状态总览

现有告警数、一般告警数、严重告警数，可以从告警模块的redis中拿到
发送给 opentsdb和MongoDB
"""
import os
import time
import sys
import json
import logging

import pymongo

from argus_statistics.utils import *

logger = logging.getLogger("alert_stat")


def update_alert(total, critical, minor):
    """Connect to mongodb and fetch the data we needed."""
    ts = int(time.time())
    send_data = {"check_time": ts,
                 "alerts": total,
                 "alert_critical": critical,
                 "alert_minor": minor,
                 }
    # print(send_data)
    send_to_db("argus-statistics", "alert_stat", send_data)
    logger.debug("update success")


def get_alert_all(alert_connection):
    alert_total = 0
    alert_critical = 0
    alert_minor = 0
    for item in alert_connection.find({"is_recover":False}):
        if item["level"] == "critical":
            alert_critical += 1
        elif item["level"] == "minor":
            alert_minor += 1
        alert_total += 1
    return (alert_total, alert_critical, alert_minor)


def main():
    logger.debug("alert_stat is starting")
    alert_col = get__mongo_cursor("argus-alert", "alert_history")
    alert_now, alert_p, alert_c = get_alert_all(alert_col)
    update_alert(alert_now, alert_p, alert_c)
    logger.debug("save count tmp file is done")
    logger.debug("finish")

if __name__ == '__main__':
    main()
