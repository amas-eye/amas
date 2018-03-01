#!/usr/bin/python
# coding=utf-8
"""
这个是用于采集Hbase相关的节点的数据，包括Master和Region_server两个角色

"""

import json
import urllib2
import time
import socket
import re
import sys
import os

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


from argus_collector.collectors.etc.hbase_config import *
from argus_collector import utils



def Charater(hostname, ip, config_path, region_conf):
    """
    this function is to findout the charater of server
    :param hostname:
    :param ip:
    :param config_path:
    :return: charater (NameNode or DataNode)
    """
    tree = ET.parse(config_path)
    root = tree.getroot()
    title = root.findall('property')
    for item in title:
        name = item.find('name').text
        value = item.find('value').text
        if name == "hbase.master.ipc.address":
            config_ip = value
            if config_ip == "0.0.0.0" or config_ip == ip:
                with open(region_conf, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line == hostname or line == ip or line == "localhost":
                            return "both"
                        else:
                            return "master"
            else:
                return "region_server"


def print_metric(metric, ts, value, tags=""):
    """
    this function is to print record to insert into opentsdb
    打印出来格式为hadoop.hbase.metric ts value tags
    :param metric:
    :param ts:
    :param value:
    :param tags:
    :return:
    """
    if tags:
        space = " "
    else:
        tags = space = ""
    print "hadoop.hbase.%s %d %s %s" % (metric, int(ts), value,
                                          tags)


def get_data(host, port, metric_list, ts, tag):
    """
    这个函数分开两个情况，master和region_server分开和master和region——server合一的两种情况
    :param host:
    :param port:
    :param metric_list:
    :param ts:
    :param tag:
    :return:
    """
    for mbean in metric_list.keys():
        if not isinstance(port, list):
            useable_content = get_jmx(host, port, mbean)
            if useable_content == 0:
                continue
            else:
                try:
                    for item in metric_list[mbean]:
                        value = useable_content[item]
                        print_metric(item, ts, value, tag)
                except KeyError:
                    continue
        else:
            if re.findall("name=Master", mbean):
                port_bmode = port[0]
            else:
                port_bmode = port[1]
            useable_content = get_jmx(host, port_bmode, mbean)
            if useable_content == 0:
                continue
            else:
                try:
                    for item in metric_list[mbean]:
                        value = useable_content[item]
                        print_metric(item, ts, value, tag)
                except KeyError:
                    continue


def get_jmx(host, port, mbean):
    try:
        jmx_site = "http://{host}:{port}/jmx?qry={mbean}".format(host=host,
                                                             port=port, mbean=mbean)
        origin_response = urllib2.urlopen(jmx_site)
        response_content = origin_response.read()
        useable_content = json.loads(response_content)['beans'][0]
        return useable_content
    except IndexError:
        return 0


def main():
    TIME_INTERVAL = os.path.basename(os.path.dirname((os.path.abspath(__file__)))).strip()
    confdir = config_path
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    region_conf_file = region_file
    if manual_charater == None:
        charater = Charater(hostname, ip, confdir, region_conf_file)
    else:
        charater = manual_charater
    if charater == "master":
        metric_list = master_metric
        port = master_port
        tag = "node=master"
    elif charater == "region_server":
        metric_list = region_server_metric
        port = region_port
        tag = "node=region_server"
    else:
        port = [master_port, region_port]
        tag = "node0=master node1=region_server"
        metric_list = dict(master_metric, **region_server_metric)

    # hosttag = "host={hostname} ".format(hostname=hostname)
    hosttag = ""
    tags = "{hosttag}{tag}".format(hosttag=hosttag, tag=tag)
    ts = time.time()
    get_data(host, port, metric_list, ts, tags)
    sys.stdout.flush()

if __name__ == "__main__":
    sys.exit(main())