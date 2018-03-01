#!/usr/bin/python
# coding=utf8
"""
这个是用于对mysql进行性能监控的采集脚本
"""
import os
import sys
import json
import time

import pymysql
from pymysql import OperationalError

from argus_collector.collectors.etc.mysql_conf import *


def connect_mysql(host, username, password, port):
    """
    连接到数据，返回一个连接的对象
    :param host:
    :param username:
    :param password:
    :param port:
    :return:
    """
    try:
        connection = pymysql.connect(host=host,
                                     user=username,
                                     password=password,
                                     cursorclass=pymysql.cursors.DictCursor,
                                     port=port)
        return connection
    except OperationalError:
        print "请检查你在配置的问题，或者检查你的mysql日志看看mysql进程是否存在"


def get_default_storage_engine(db_cursor):
    """
    因为mysql不同引擎会有不同的特点，因此要对默认引擎类型进行判断
    :param db_cursor:
    :return:
    """
    get_storage_type_sql = 'show variables like "%\storage_engine%"'
    db_cursor.execute(get_storage_type_sql)
    data = db_cursor.fetchall()  # 此处获取到的是List
    engine_type = ""
    for item in data:
        if item["Variable_name"] == "default_storage_engine":
            engine_type = item["Value"]
    return {"key": "engine_type", "value": engine_type}


def check_slow_query(db_cursor):
    sql = "show variables like 'slow_query%'"
    db_cursor.execute(sql)
    slow_query_status = ""
    for item in db_cursor.fetchall():
        if item["Variable_name"] == "slow_query_log":
            slow_query_status = item["Value"]
    return {"key": "slow_query", "value": slow_query_status}


def get_character(db_cusror):
    """
    判断mysql集群中的角色，针对不同角色有分类的监控
    :param db_cusror:
    :return:
    """
    slave_sql = "show slave status"
    datanum = db_cusror.execute(slave_sql)
    if datanum == 0:
        return "master"
    else:
        return "slave"


def get_data_from_status(db_cursor, metric_list):
    sql = "show status"
    db_cursor.execute(sql)
    data = db_cursor.fetchall()
    store_dict = {}
    ts = int(time.time())
    print_str = ""
    base_metric_head = "mysql"
    for item in data:
        store_dict[item["Variable_name"]] = item["Value"]
    for singleitem in metric_list:
        v = store_dict[singleitem]
        if not "Innodb" in singleitem:
            metric_head = "mysql.performance"
        else:
            metric_head = base_metric_head
        every_str = "{mh}.{item} {ts} {value} {ta}".format(
            mh=metric_head,
            item=singleitem,
            ts=ts,
            value=v,
            ta=""
        )
        print_str = "{origin} \n{s}".format(origin=print_str,
                                            s=every_str)
    return print_str


def define_slave_alive(db_cursor, printstr):
    sql = "show slave status"
    db_cursor.execute(sql)
    data = db_cursor.fetchall()
    data_dict = data[0]
    ts = int(time.time())
    metric = "mysql.slave.alive"
    if data_dict["Slave_SQL_Running"] == "Yes" and data_dict["Slave_SQL_Running"] == "Yes":
        value = 1
        alive_str = "{m} {ts} {v} {ta} \n".format(m=metric,
                                                  ts=ts,
                                                  v=value,
                                                  ta=""
                                                  )
        return "{pstr} \n{alivestr}".format(pstr=printstr, alivestr=alive_str)
    else:
        value = 0
        alive_str = "{m} {ts} {v} {ta} \n".format(m=metric,
                                                  ts=ts,
                                                  v=value,
                                                  ta=""
                                                  )
        return "{pstr} \n{alivestr}".format(pstr=printstr, alivestr=alive_str)


def load_config(configfile, db_cursor):
    if os.path.exists(configfile):
        value_dict = {}
        with open(configfile, "rb") as f:
            for i in f:
                i = json.loads(i)
                value_dict[i["key"]] = i["value"]
        return value_dict
    else:
        engine_type = get_default_storage_engine(db_cursor)
        slow_query = check_slow_query(db_cursor)
        value_dict = {}
        write_list = [engine_type, slow_query]
        for wlitem in write_list:
            value_dict[wlitem['key']] = wlitem['value']
        with open(configfile, "wb") as wf:
            for item in write_list:
                data = json.dumps(item)
                wdata = "{d}\n".format(d=data)
                wf.write(wdata)
        return value_dict


status_metric_list = [
    "Innodb_buffer_pool_pages_free", "Innodb_buffer_pool_pages_total",
    "Innodb_row_lock_current_waits", "Innodb_data_reads",
    "Innodb_data_writes", "Innodb_os_log_fsyncs",
    "Innodb_row_lock_time", "Innodb_row_lock_waits",
    "Max_used_connections", "Com_delete",
    "Com_delete_multi", "Com_insert", "Com_insert_select",
    "Com_replace_select", "Com_select", "Com_update",
    "Com_update_multi", "Created_tmp_disk_tables",
    "Created_tmp_files", "Created_tmp_tables",
    "Open_files", "Open_tables",
    "Qcache_hits", "Queries", "Questions",
    "Slow_queries", "Table_locks_waited",
    "Threads_connected", "Threads_running",
    "Com_lock_tables",
]


def main():
    connection = connect_mysql(MYSQL_HOST,
                               MYSQL_USER_NAME,
                               MYSQL_USER_PASSWORD,
                               int(MYSQL_PORT),
                               )
    cursor = connection.cursor()
    tmpfilepath = "{dirpath}/{dirname}".format(
        dirpath=os.path.dirname(os.path.dirname(__file__)),
        dirname='data'
    )
    tmpfile = "{p}/{f}".format(p=tmpfilepath, f="mysql.data")
    print tmpfilepath
    config_dict = load_config(tmpfile, cursor)
    print config_dict
    charater = get_character(cursor)
    if charater == "master":
        pstr = get_data_from_status(cursor, status_metric_list)
        print pstr
    else:
        pstr = get_data_from_status(cursor, status_metric_list)
        pstr = define_slave_alive(cursor, pstr)
        print pstr


if __name__ == "__main__":
    sys.exit(main())
