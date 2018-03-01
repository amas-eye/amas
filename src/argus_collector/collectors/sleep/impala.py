#!/usr/bin/python
# coding=utf8
"""
对于base_metric，获得对象为列表，只需先判断name，然后取value值
"""

import sys
import re
import socket
import urllib2
import json
import time

from argus_collector.collectors.etc.impala_conf import *


def main():
    def get_character(conf_path, host_ip):
        with open(conf_path, "r") as f:
            lines = f.xreadlines()
            catalog_host = re.compile("IMPALA_CATALOG_SERVICE_HOST")
            state_store = re.compile("IMPALA_STATE_STORE_HOST")
            characters = "impalad"
            for line in lines:
                if re.match(catalog_host, line):
                    line_split = line.split("=")
                    catalog_server_ip = line_split[1].rstrip()
                    if catalog_server_ip == host_ip or catalog_server_ip == "127.0.0.1":
                        characters = "{c} catalog".format(c=characters)
                elif re.match(state_store, line):
                    line_split = line.split("=")
                    state_store_ip = line_split[1].rstrip()
                    if state_store_ip == host_ip or state_store_ip == "127.0.0.1":
                        characters = "{c} statestore".format(c=characters)
            print characters
            return characters

    def send_request(url):
        try:
            response = urllib2.urlopen(url=url)
            data = response.read()
            json_data = json.loads(data)
            return json_data
        except urllib2.URLError:
            print "请检查你的端口和防火墙配置是否正确，或者业务是否已经启动"

    def get_data(function_port):
        """
        只需套入不同角色所拥有的端口号，即可获得对应服务的json数据采集信息
        :param function_port:
        :return:
        """
        url = "http://127.0.0.1:{p}/metrics?json".format(p=function_port)
        response_data = send_request(url)
        return response_data

    def get_value_key(data):
        value_dict = {}
        value_key = "value"
        name_key = "name"
        for singleitem in data:
            try:
                value_dict[singleitem[name_key]] = singleitem[value_key]
            except KeyError:
                print "this item has not value attr"
        return value_dict

    def get_other_key(data, metric_name, keylist):
        value_dict = {}
        name_key = "name"
        value_key_list = keylist
        for singleitem in data:
            if singleitem[name_key] == metric_name:
                for key in value_key_list:
                    save_key = "{origin}.{k}".format(origin=singleitem[name_key], k=key)
                    value_dict[save_key] = singleitem[key]
        return value_dict

    def parse_impala(response, metric):
        """
        :param response:type==json
        :param metric:
        :return:
        """
        data = response
        metric_data = data["metric_group"]["metrics"]  # 得到类型为list
        other_data = data["metric_group"]["child_groups"]
        schdule_data = []
        server_data = []
        statestore_data = []
        for i in other_data:
            if i["name"] == "impala-server":
                server_data = i["metrics"]
            elif i["name"] == "scheduler":
                schdule_data = i["metrics"]
            elif i["name"] == "statestore-subscriber":
                statestore_data = i["metrics"]
        for item in metric.keys():
            if item == "base_metric":
                match_dict = {}
                get_value_key_dict = get_value_key(metric_data)
                match_dict = dict(match_dict, **get_value_key_dict)
                pipei_item = "statestore-subscriber.heartbeat-interval-time"
                key_list = ["mean", "min", "max", "last", "stddev"]
                get_other_dict = get_other_key(metric_data, pipei_item, key_list)
                match_dict = dict(match_dict, **get_other_dict)
                for m in impalad_base_dict.keys():
                    value = match_dict[m]
                    ts = int(time.time())
                    metric = m
                    front = "impalad"
                    print_data(metric, ts, value, front)
            else:
                if item == "schdule_metric":
                    schdule_dict = {}
                    for singleitem in schdule_data:
                        if singleitem["name"] == "simple-scheduler.num-backends":
                            schdule_dict[singleitem["name"]] = singleitem["value"]
                    for m in impalad_schdule_dict.keys():
                        value = schdule_dict[m]
                        ts = int(time.time())
                        metric = m
                        front = "impalad"
                        print_data(metric, ts, value , front)
                elif item == "statestore_metric":
                    state_dict = {}
                    for singleitem in statestore_data:
                        if singleitem["name"] == "statestore-subscriber.last-recovery-time":
                            v = singleitem["value"]
                            if v == "N/A":
                                v = 0
                            state_dict[singleitem["name"]] = v
                    for m in impalad_statestore_dict.keys():
                        value = state_dict[m]
                        ts = int(time.time())
                        metric = m
                        front = "impalad"
                        print_data(metric, ts, value, front)
                elif item == "server_metric":
                    server_dict = {}
                    keynames = [
                            "25th %-ile", "50th %-ile", "75th %-ile",
                            "90th %-ile", "95th %-ile", "99.9th %-ile", "count",
                        ]
                    metric = "impala-server.ddl-durations-ms"
                    metric_dict = get_other_key(server_data, metric, keynames)
                    for k in metric_dict.keys():
                        if re.findall(r"\s+", k):
                            tempory_value = metric_dict[k]
                            origin_k = k
                            k = k.replace(" ", "")
                            k = k.replace("%", "percent")
                            metric_dict[k] = tempory_value
                            del(metric_dict[origin_k])
                    server_dict = dict(server_dict, **metric_dict)
                    metric_dict2 = get_value_key(server_data)
                    server_dict = dict(server_dict, **metric_dict2)
                    for m in impalad_server_dict.keys():
                        value = server_dict[m]
                        ts = int(time.time())
                        metric = m
                        front = "impalad"
                        print_data(metric, ts, value, front)

    def parse_catalog(response, metric_dict):
        data = response
        data = data['metric_group']['metrics']
        catalog_dict = {}
        for item in metric_dict.keys():
            if item == "base":
                get_value_dict = get_value_key(data)
                catalog_dict = dict(catalog_dict, **get_value_dict)
                metric_name = "statestore-subscriber.heartbeat-interval-time"
                keylist = ["min", "max", "last"]
                get_other_dict = get_other_key(data, metric_name, keylist)
                catalog_dict = dict(catalog_dict, **get_other_dict)
            else:
                get_value_dict = get_value_key(data)
                catalog_dict = dict(catalog_dict, **get_value_dict)
        for m in catalog_base_metric_dict.keys():
            value = catalog_dict[m]
            ts = int(time.time())
            metric = m
            front = "catalogd"
            print_data(metric, ts, value, front)

    def parse_statestore(response):
        data = response
        data = data['metric_group']['metrics']
        statestore_value_dict = {}
        get_value_dict = get_value_key(data)
        statestore_value_dict = dict(statestore_value_dict, **get_value_dict)
        for m in statestore_dict.keys():
            value = statestore_value_dict[m]
            ts = int(time.time())
            metric = m
            front = "statestored"
            print_data(metric, ts, value, front)

    def print_data(metric, timestamp, value, front):
        print "{f}.{m} {t} {v} ".format(f=front, m=metric, t=timestamp, v=value)

    catalog_base_metric_dict = {
        "statestore-subscriber.heartbeat-interval-time.min": "min",
        "statestore-subscriber.heartbeat-interval-time.max": "max",
        "statestore-subscriber.heartbeat-interval-time.last": "last",
        # "statestore-subscriber.heartbeat-interval-time.avg": "avg",
        "tcmalloc.bytes-in-use": "value",
        "tcmalloc.pageheap-free-bytes": "value",
        "tcmalloc.pageheap-unmapped-bytes": "value",
        "tcmalloc.physical-bytes-reserved": "value",
        "tcmalloc.total-bytes-reserved": "value",
        "statestore-subscriber.statestore.client-cache.total-clients": "value",
        "statestore-subscriber.statestore.client-cache.clients-in-use": "value",
        "impala.thrift-server.CatalogService.connections-in-use": "value",
        "impala.thrift-server.CatalogService.total-connections": "value",
    }

    catalog_statestore_metric = {
        "statestore-subscriber.last-recovery-duration": "value",
    }

    statestore_dict = {
        "statestore.live-backends": "value",
        "statestore.total-key-size-bytes": "value",
        "statestore.total-topic-size-bytes": "value",
        "statestore.total-value-size-bytes": "value",
        "subscriber-heartbeat.client-cache.clients-in-use": "value",
        "subscriber-heartbeat.client-cache.total-clients": "value",
        "tcmalloc.bytes-in-use": "value",
        "tcmalloc.pageheap-free-bytes": "value",
        "tcmalloc.pageheap-unmapped-bytes": "value",
        "tcmalloc.physical-bytes-reserved": "value",
        "tcmalloc.total-bytes-reserved": "value",
        "thread-manager.running-threads": "value",
        "thread-manager.total-threads-created": "value",
    }

    impalad_base_dict = {
        "tcmalloc.bytes-in-use": "value",
        "tcmalloc.pageheap-free-bytes": "value",
        "tcmalloc.pageheap-unmapped-bytes": "value",
        "tcmalloc.physical-bytes-reserved": "value",
        "tcmalloc.total-bytes-reserved": "value",
        "thread-manager.running-threads": "value",
        "thread-manager.total-threads-created": "value",
        "impala.thrift-server.hiveserver2-frontend.total-connections": "value",
        "impala.thrift-server.hiveserver2-frontend.connections-in-use": "value",
        "mem-tracker.process.bytes-freed-by-last-gc": "value",
        "mem-tracker.process.bytes-over-limit": "value",
        "statestore-subscriber.heartbeat-interval-time.last": "last",
        "statestore-subscriber.heartbeat-interval-time.max": "max",
        "statestore-subscriber.heartbeat-interval-time.min": "min",
        "statestore-subscriber.heartbeat-interval-time.mean": "mean",
        "statestore-subscriber.heartbeat-interval-time.stddev": "sttdev",
        "statestore-subscriber.statestore.client-cache.clients-in-use": "value",
        "statestore-subscriber.statestore.client-cache.total-clients": "value",
    }

    impalad_schdule_dict = {
        "simple-scheduler.num-backends": "value",
    }

    impalad_statestore_dict = {
        "statestore-subscriber.last-recovery-time": "value",
    }

    impalad_server_dict = {
        "impala-server.ddl-durations-ms.25thpercent-ile": "25th %-ile",
        "impala-server.ddl-durations-ms.50thpercent-ile": "50th %-ile",
        "impala-server.ddl-durations-ms.75thpercent-ile": "75th %-ile",
        "impala-server.ddl-durations-ms.90thpercent-ile": "90th %-ile",
        "impala-server.ddl-durations-ms.95thpercent-ile": "95th %-ile",
        "impala-server.ddl-durations-ms.99.9thpercent-ile": "99.9th %-ile",
        "impala-server.ddl-durations-ms.count": "count",
        "impala-server.io-mgr.cached-bytes-read": "value",
        "impala-server.io-mgr.bytes-written": "value",
        "impala-server.io-mgr.bytes-read": "value",
        "impala-server.io-mgr.local-bytes-read": "value",
        "impala-server.io-mgr.total-bytes": "value",
        "impala-server.mem-pool.total-bytes": "value",
        "impala-server.scan-ranges.total": "value",
        "impala-server.scan-ranges.num-missing-volume-id": "value",
        "impala-server.num-queries-expired": "value",
        "impala-server.num-sessions-expired": "value",
        "impala-server.hash-table.total-bytes": "value",
    }

    impalad_total_dict = {
        "base_metric": impalad_base_dict,
        "schdule_metric": impalad_schdule_dict,
        "server_metric": impalad_server_dict,
        "statestore_metric": impalad_statestore_dict
    }

    catalog_total_dict = {
        "base": catalog_base_metric_dict,
        "other": catalog_statestore_metric
    }

    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    character = get_character(IMPALA_CONF_PATH, ip)
    # character_split = character.split(" ")
    if character == "impalad":
        data_port = IMPALA_CONFIG_PORT
        response = get_data(data_port)
        parse_impala(response, impalad_total_dict)

    elif character == "impalad catalog":
        data_port = [IMPALA_CONFIG_PORT, CATALOG_PORT]
        for port in data_port:
            response = get_data(port)
            if port == IMPALA_CONFIG_PORT:
                parse_impala(response, impalad_total_dict)
            else:
                parse_catalog(response, catalog_total_dict)
    elif character == "impalad statestore":
        data_port = [IMPALA_CONFIG_PORT, STATESTORE_PORT]
        for port in data_port:
            response = get_data(port)
            if port == IMPALA_CONFIG_PORT:
                parse_impala(response, impalad_total_dict)
            else:
                parse_statestore(response)
    else:
        data_port = [IMPALA_CONFIG_PORT, STATESTORE_PORT, CATALOG_PORT]
        for port in data_port:
            response = get_data(port)
            if port == IMPALA_CONFIG_PORT:
                parse_impala(response, impalad_total_dict)
            elif port == CATALOG_PORT:
                parse_catalog(response, catalog_total_dict)
            else:
                parse_statestore(response)


if __name__ == "__main__":
    sys.exit(main())
