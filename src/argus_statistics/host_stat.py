# coding=utf-8
"""
主机的状态统计 以及健康度更新
"""

import os
import json
import logging
import time
from urllib.error import URLError

from argus_statistics.utils import *
from argus_statistics.settings import *

current_dir = os.getcwd()
config_dir = current_dir + "/etc/host_config.json"
logger = logging.getLogger("host_stat")

def update_host(senddata: dict):
    """Connect to Mongodb and fetch the newest data we collect.
    senddata format:
    {
        "hosts": 50,
        "hosts_normal": 40,
        "hosts_error": 8,
        "hosts_closed": 2
    }
    """
    ts = int(time.time())
    senddata["check_time"] = ts
    # print(senddata)
    send_to_db("argus-statistics", "host_stat", senddata)
    logger.debug("update success")


def update_health(health: int):
    ts = int(time.time())
    send_data = {}
    send_data["check_time"] = ts
    send_data["score"] = health
    send_to_db("argus-statistics", "overall_health", send_data)
    logger.debug("update success")
    print(f'Updated to db! Now system health is {health}')

def read_config(conf_dir: str):
    """
    读取配置文件
    :param conf_dir:
    :return:
    """
    with open(conf_dir, "rb") as f:
        config = f.read()
        config_dict = json.loads(config)
        host_total = int(config_dict["host_total_num"])
        manage_host = config_dict["manage_host"]
        manage_port = int(config_dict["manage_port"])
        classify = config_dict['classify']
        logger.debug("config reading success")
        return (host_total, manage_host, manage_port, classify)


def save_config(conf_dir: str, count: int):
    """
    当用户没有配置机器数的时候，进行自动检测，然后把检测到的主机数保存到配置中
    :param conf_dir:
    :param count:
    :return:
    """
    f = open(conf_dir, "rb")
    data = json.loads(f.read())
    f.close()
    with open(conf_dir, "wb") as wf:
        data["host_total_num"] = str(count)
        config_new = json.dumps(data)
        config_new = bytes(config_new, encoding="utf-8")
        print(config_new)
        wf.write(config_new)
    logger.debug("save config done")


def get_host_by_system():
    """
    这个函数是用于通过通用metric来自动进行主机发现，当使用者没有进行主机总数配置的情况下
    返回一个所有主机数
    :return: int:host_total_num
    """
    result = check_tsdb()
    if result:
        count = 0
        tsdhost = OPENTSDB_HOST
        tsdport = OPENTSDB_PORT
        interval_time = 3 * 60
        metric_name = "cluster.cpu.usage"
        baseurl = 'http://{tsd}:{p}/api/query?'.format(tsd=tsdhost, p=tsdport)
        param = {}
        param["start"] = "{interval}s-ago".format(interval=interval_time)
        param["m"] = "max:{metric}{add}".format(metric=metric_name,
                                                add="{host=*}"
                                                )
        response = urlopen(base_url=baseurl, param=param)
        json_response = json.loads(response.read())
        for i in json_response:
            if i:
                count += 1
        return count
    else:
        logger.log("DEBUG", "tsd connected fail")


def get_alert_host(alist :list):
    col = get__mongo_cursor('argus-alert','alert-history')
    for item in col.find():
        if item['is_recover'] != True:
            host = item['group'].split('=')[2]
            if host not in alist:
                alist.append(host)


def get_alive_host_num(M_host: str, M_port: int, min_interval: int, max_interval :int, alist: list):
    """
    通过采集管理api进行对存活的agent数量的统计，返回用于计算关闭的机器
    :param M_host:
    :param M_port:
    :param interval:
    :return:
    """
    compare_time = int(time.time())
    alive_num = 0
    close = 0
    try:
        baseurl = "http://{h}:{p}/api/collector/agent".format(h=M_host, p=M_port)
        response = urlopen(baseurl)
        data = json.loads(response.read())
        for item in data["data"]:
            try:
                if (compare_time - item["heartbeat_time"]) <min_interval:
                    alive_num += 1
                elif min_interval < (compare_time - item["heartbeat_time"]) < max_interval:
                    alist.append(item['host'])
                else:
                    close += 1
            except TypeError:
                logging.error("please check the data in api/collector/agent")
                print("please check the data in api/collector/agent")
                continue
        total = alive_num + close
        return total, alive_num, close
    except URLError:
        logger.error("api server can't connect , check your connection")
        print("api server can't connect , check your connection")
        return False

def count_alert_point(classify):
    strategy_col = get__mongo_cursor('argus-alert', 'strategy')
    if classify:
        critical_num = 0
        exist_critical = 0
        minor_num = 0
        exist_minor = 0
        # alert_col = get__mongo_cursor('argus-alert','alert-history')
        for item in strategy_col.find():
            if item['level'] == 'critical':
                critical_num += 1
                if item['status'] == 'alert':
                    exist_critical += 1
            elif item['level'] == 'minor':
                minor_num += 1
                if item['status'] == 'alert':
                    exist_minor += 1
        total_point = critical_num *3 + minor_num
        total_alert_point = exist_critical*3 + exist_minor
        inpoint = (total_alert_point /total_point) * 60
        return inpoint
    else:
        item_num = 0
        alert_num = 0
        for item in strategy_col.find():
            item_num += 1
            if item['status'] == 'alert':
                alert_num += 1
        inpoint = (alert_num / item_num) *60
        return inpoint

def main():
    alert_host = []
    max_interval = 6 * 3600
    min_interval = 3600
    total_host_num, manage_host, manage_port,classify = read_config(config_dir)
    if total_host_num == 0:
        total_host_num = get_host_by_system()
        save_config(config_dir, total_host_num)
    total_host_num, alive_host_num, close_num = get_alive_host_num(manage_host, manage_port, min_interval, max_interval,
                                                                   alert_host)
    get_alert_host(alert_host)
    fail_host_num = len(alert_host)
    fail_host_point = (fail_host_num / total_host_num) * 40
    alert_point = count_alert_point(classify)
    health = int(100 - alert_point - fail_host_point)
    host_data = {
        "hosts": total_host_num,
        "hosts_normal": alive_host_num,
        "hosts_error": fail_host_num,
        "hosts_closed": close_num
    }
    update_host(host_data)
    update_health(health)
    logger.debug("finish")

if __name__ == '__main__':
    main()
