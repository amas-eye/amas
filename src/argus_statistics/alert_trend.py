#!/usr/bin/python3
# coding=utf-8
"""
告警趋势数据，按小时进行分类
"""
import os
import time
import logging

from argus_statistics.utils import *

logger = logging.getLogger("alert_trend")



def get_period_data( st, et):
    """
    :param st: 开始时间(UnixTime)
    :param et: 结束时间(unixTime)
    :return:
     result , 顺序为参数数量， 取消数量， 严重数量， 一般数量
    """
    col = get__mongo_cursor("argus-alert", "alert_history")
    produce = 0
    canel = 0
    critical = 0
    minor = 0
    for item in col.find({"alert_time":{"$gt":st,"$lt":et}}):
        if item["is_recover"] == True:
            canel += 1
        if item["level"] == "critical":
            critical += 1
        elif item["level"] == "minor":
            minor += 1
        produce += 1
    return (produce, canel, critical, minor)


def update_alert(result ,ts, st, et):
    """Connect to mongodb and fetch the data we needed."""
    send_data = {"check_time": ts,
                 "start_time":st,
                 "end_time": et,
                 "period_alert_produce": result[0],
                 "period_alert_canel": result[1],
                 "period_critical_alert": result[2],
                 "period_minor_alert": result[3]
                 }
    query_dict = {"start_time":{"$gte":st}}
    update_data = {"$set":send_data}
    col = get__mongo_cursor("argus-statistics", "alert_trend")
    qdata = col.find_one({"start_time":{"$gte":st}})
    if not qdata:
        send_to_db("argus-statistics", "alert_trend", send_data)
    else:
        update_to_db(query_dict,"argus-statistics", "alert_trend", update_data)


def main():
    worktime = int(time.time())
    starttime = (worktime//3600)*3600
    endtime = starttime + 3600
    result = get_period_data(starttime, endtime)
    update_alert(result, worktime,starttime, endtime)
    logger.debug("done")


if __name__ == '__main__':
    main()