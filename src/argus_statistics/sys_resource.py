#!/usr/bin/env/python
# coding=utf-8
"""系统基础资源统计数据

CPU、内存、硬盘、网络流量的总计和TOP5
依赖于采集器：CPU、内存、硬盘和网络的源数据采集
"""
import os
import json
import heapq
import logging
import time

# from argus-extsvr.argus_statistics.utils import get_client, urlopen
from argus_statistics.utils import get_client, urlopen, send_to_db, check_tsdb, check_scale

tsd_host = ""
tsd_port = 0
db = "argus-statistics"
top_collection = "sys_resource"
# TSDB_HOST = '10.17.35.43'
TSDB_HOST = "192.168.0.253"
# TSDB_HOST = '192.168.232.128'
TSDB_PORT = 4242
interval_time = 10 * 60  # senconds

logger = logging.getLogger("top 5 module")

def update_sys_resource():
    """Fetch the data we needed and insert into MongoDB."""

    cpu_cores = get_cpu_cores()
    logger.debug("starting top module")
    cpu_usage = get_cpu_usage()
    mem_usage = get_mem_usage()
    df_usage = get_df_usage()
    logger.debug("round instrument data ready, next is top 5data")
    fields = [
        'check_time', 'cpu_usage', 'cpu_all', 'cpu_using', 'mem_usage',
        'mem_all', 'mem_using', 'disk_usage', 'disk_all', 'disk_using',
        'cpu_topN', 'mem_topN', 'disk_topN', 'net_in_topN', 'net_out_topN'
    ]
    # result = {}
    # result.fromkeys(field, None)
    result = {i: None for i in fields}
    result['check_time'] = int(time.time())
    result['cpu_all'] = cpu_cores
    result['cpu_usage'] = cpu_usage
    result['mem_all'], result['mem_using'] = mem_usage
    result['disk_all'], result['disk_using'] = df_usage
    result['mem_usage'] = result['mem_using'] / result['mem_all']
    result['disk_usage'] = result['disk_using'] / result['disk_all']
    result['cpu_topN'] = get_topN_cpu()
    net_topn_data = get_topN_netIO()
    mnd_topn_data = get_topN_mnd()
    result["mem_topN"] = mnd_topn_data["mem.bytes.memavailable"]
    result["disk_topN"] = mnd_topn_data["df.bytes.used"]
    result["net_in_topN"] = net_topn_data["cluster.net.dev.receive"]
    result["net_out_topN"] = net_topn_data["cluster.net.dev.transmit"]
    # print(result)
    send_to_db('argus-statistics', 'sys_resource', result)
    logger.debug("update is already success")


def get_cpu_cores():
    """
    Use metric <cluster.cpu.usage>.

    /api/query/?start=10m-ago&m=sum:cluster.cpu.cores{host=*}
    """
    cluster_count, cores = get_usage("cluster.cpu.cores", interval_time)

    return cores

def get_cpu_usage():
    """
    Use metric <cluster.cpu.usage>.

    /api/query/?start=10m-ago&m=sum:cluster.cpu.usage{host=*}
    """

    count, sum_result = get_usage("cluster.cpu.usage", interval_time)

    return sum_result / count if count else float(count)


def get_mem_usage():
    """
    Use metric <mem.bytes.memtotal> <mem.bytes.used>.

    return: (int, int) first element represent total, 2th is sum of used memory
    rtype: tuple
    """

    total_count, total_sum = get_usage('mem.bytes.memtotal', interval_time)
    used_count, used_sum = get_usage('mem.bytes.used', interval_time)

    return (total_sum, used_sum)


def get_df_usage():
    """
    Use metric: <df.bytes.total> <df.bytes.used>.

    return: (int, int) first element represent total disk amout, 2th is sum of used disk
    rtype: tuple
    """

    total_count, total_sum = get_usage('df.bytes.total', interval_time)
    used_count, used_sum = get_usage('df.bytes.used', interval_time)

    return (total_sum, used_sum)


def get_usage(metric: str, interval_time: int):
    r"""Get specific metric's useful info.

    :param metric: Metric name need to be gotten.
    :param invertal_time: Start parameter in api request i.e. start=300s-ago, use second as unit.
    :return: (int, int) represent the cluster scale and sum of latest time series at query time
    :rtype: tuple Object with 2 elements both are int.
    """

    count, ignored = check_scale(metric, f'{interval_time}s')
    param = {
        'start': f'{interval_time}s-ago',
        'm': f'sum:{metric}' + '{host=*}',
    }

    start = time.time()
    resp = urlopen(f'http://{TSDB_HOST}:{TSDB_PORT}/api/query?', param)
    if resp.status == 200:
        _total = json.load(resp)
    else:
        pass

    # remove the elements that should be ignored
    valid_source = [i for i in _total if i['tags'] not in ignored]

    valid_last_time = []
    for i in valid_source:
        last = sorted(i['dps'].keys())[-1]
        if (start - interval_time) <= int(last) <= (start + interval_time):
            valid_last_time.append(i)
        else:
            pass
    # elements in valid_last_time mean it should be aggregated.
    total = [i['dps'][sorted(i['dps'].keys())[-1]] for i in valid_last_time]

    return (count, sum(total))


def get_raw_data(url, Param):
    """
    这个是公用方法，用于从TSDB中获取数据, 并且把数据进行提取（获取最新数据和对应的host
    原数据：
    {"metric":"mem.bytes.memavailable","tags":{"host":"cdh180"},"aggregateTags":[],"dps":{"1510535675":12250939392}}
    处理后数据：
    {host:"cdh180", "data" = "12250939392"}
    :param url:
    :param Param:
    :return:
    """
    response = urlopen(url, Param)
    if response.status == 200:
        response_data = json.load(response)
        available_data = []
        for item in response_data:
            single_data = {}
            host = item["tags"]["host"]
            if item["dps"] == {}:
                continue
            newest_key = list(item["dps"].keys())[-1]
            data = item["dps"][newest_key]
            single_data["host"] = host
            single_data["data"] = data
            available_data.append(single_data)
        return available_data
    else:
        return 0


def sorting_data(a_data, metric_name):
    """
    输入：
    [{"host":"cdh180", "data":1234}, {"host":"cdh182","data":55555}, {"host":"cdh251", "data":3333}]
    输出：
    [{'data': 1234, 'host': 'cdh180'},{'data': 3333, 'host': 'cdh251'},{'data': 55555, 'host': 'cdh182'}]
    :param a_data: get_raw_data中拿到的结果类型
    :return: sorted_data (type:list)
    """
    normal = ("cluster.cpu.usage", "cluster.net.dev.receive", "cluster.net.dev.transmit")
    if metric_name  in normal:
        sorted_data = sorted(a_data, key=lambda k:k['data'], reverse=True)
    else:
        sorted_data = sorted(a_data, key=lambda k: k['per'], reverse=True)
    return sorted_data


def add_percentage(s_data, metric_name):
    """
    这是以一个公用的方法
    输入：
    [{'data': 1234, 'host': 'cdh180'},{'data': 3333, 'host': 'cdh251'},{'data': 55555, 'host': 'cdh182'}]
    输出：
    [{'data': 1234, 'host': 'cdh180',"per":1},{'data': 3333, 'host': 'cdh251',"per":10},
    {'data': 55555, 'host': 'cdh182',"per":100}]
    :param s_data: 已经排序好的列表
    :return:
    """
    max_data = s_data[0]['data']
    normal = ("cluster.cpu.usage", "cluster.net.dev.receive", "cluster.net.dev.transmit")
    for item in s_data:
        item_data = item["data"]
        if metric_name in normal:
            item["usage"] = round(item_data, 2)
            # item["per"] = round(percentage*100, 2)
            if metric_name == "cluster.cpu.usage":
                item["per"] = item["usage"] * 100
                percent_str = round(item["per"] , 2)
                item["usageprint"] = f'{percent_str}%'
            else:
                percentage = round(item_data / max_data, 2)
                item["per"] = round(percentage * 100, 2)
                item["usageprint"] = tranfor_printusage(item["data"])
        else:
            item["usage"] = item_data
            item["usageprint"] = tranfor_printusage(item["data"])
        del(item["data"])
    return s_data


def tranfor_printusage(usage):
    """
    进行单位转换的函数
    :param usage:
    :return:
    """
    unit_data = tranfer_unit(usage)
    return unit_data


def get_raw_data_formnd(url, Param):
    """
    把内存和硬盘的数据专门拿出来读取，因为处理逻辑不一样，如果耦合在一起，代码很难进行改动
    :param url:
    :param Param:
    :return:
    """
    response = urlopen(url, Param)
    if response.status == 200:
        response_data = json.load(response)
        return response_data
    else:
        return 0

def get_topN_cpu():
    """
    这里是处理top5 cpu占用路的函数
    :return:
    """
    metric = "cluster.cpu.usage"
    url = f"http://{TSDB_HOST}:{TSDB_PORT}/api/query?"
    param = {'start': '10m-ago', 'm': f'sum:{metric}' + '{host=*}'}
    metric_data = get_raw_data(url, param)
    sort_data = sorting_data(metric_data, metric)[-5:]
    sort_data = add_percentage(sort_data, metric)
    return (sort_data)


def get_mnd_usage(m_data, t_data):
    available_data = []
    count = 0
    for item in m_data:
        single_data = {}
        single_data["host"] = item["tags"]["host"]
        if item["dps"] != {}:
            single_data_key = list(item["dps"].keys())[-1]
            single_data["data"] = item["dps"][single_data_key]
            total_single_key = list(t_data[count]["dps"].keys())[-1]
            total_single_data = t_data[count]["dps"][total_single_key]
            single_data["per"] = round(single_data["data"] / total_single_data, 2) * 100
            count += 1
            available_data.append(single_data)
        else:
            continue
    return available_data


def get_topN_mnd():
    """
    这里是处理top5磁盘使用率和内存使用率的函数
    :return:
    """
    metrics = ("mem.bytes.memavailable", "df.bytes.used")
    total_metrics = ("mem.bytes.memtotal", "df.bytes.total")
    url = f"http://{TSDB_HOST}:{TSDB_PORT}/api/query?"
    data_dict = {}
    for metric in metrics:
        param = {'start': '10m-ago', 'm': f'sum:{metric}' + '{host=*}'}
        if metric == "df.bytes.used":
            total_item = "df.bytes.total"
        else:
            total_item = "mem.bytes.memtotal"
        total_param = {'start': '5m-ago', 'm': f'sum:{total_item}' + '{host=*}'}
        metric_data = get_raw_data_formnd(url, param)
        total_metric_data = get_raw_data_formnd(url, total_param)
        available_data = get_mnd_usage(metric_data, total_metric_data)
        sorted_data = sorting_data(available_data, metric)
        sort_data = add_percentage(sorted_data, metric)
        data_dict[metric] = sort_data
    # print(data_dict)
    return(data_dict)


def get_topN_netIO():
    """
    这里是处理top5网络流入流出的函数
    :return:
    """
    metrics = ("cluster.net.dev.receive", "cluster.net.dev.transmit")
    url = f"http://{TSDB_HOST}:{TSDB_PORT}/api/query?"
    data_dict = {}
    for metric in metrics:
        param = {'start':'10m-ago', 'm':f'sum:{metric}'+'{host=*}'}
        metric_data = get_raw_data(url, param)
        sort_data = sorting_data(metric_data, metric)[-5:]
        sort_data = add_percentage(sort_data, metric)
        data_dict[metric] = sort_data
    # print(data_dict)
    return(data_dict)


def tranfer_unit(number):
    """
    this function is for tranfer byte into different unit
    :param number:
    :return:
    """
    count = 0
    unit_name = ""
    if 2**20>number>2**10:
        unit_name = "Kb"
        count = 1
    elif 2**30>number>2**20:
        unit_name = "Mb"
        count = 2
    elif number>2**30:
        unit_name = "Gb"
        count = 3
    else:
        unit_name = "b"
    if count != 0 :
        unit_number = round(number / ((2**10)**count) ,2)
    else:
        unit_number = round(number, 2)
    unit_str = "{num}{name}".format(num=unit_number, name=unit_name)
    return unit_str


if __name__ == '__main__':
    update_sys_resource()
    # get_topN_cpu()
    # get_topN_netIO()
    # get_topN_mnd()