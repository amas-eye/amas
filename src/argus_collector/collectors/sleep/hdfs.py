#!/usr/bin/python
# coding=utf8

"""
这个是用于监控HDFS的运行状态的，采集以下指标:
对于NameNode：
  - hadoop.hdfs.VolumeFailuretotal
  - hadoop.hdfs.NumStaleDataNodes
  - hadoop.hdfs.NumStaleStorage
  - hadoop.hdfs.CorruptBlocks
  - hadoop.hdfs.CapacityRemain
  - hadoop.hdfs.NumLiveDataNode
  - hadoop.hdfs.NumDeadDataNode
  - hadoop.hdfs.Snapshot
  - hadoop.hdfs.Livenode

对于DataNode：
  - hadoop.hdfs.BlockVerificationFailures
  - hadoop.hdfs.BlockReportsAvgTime
  - hadoop.hdfs.BlockReportsNumOps
  - hadoop.hdfs.HeartbeatsAvgTime
  - hadoop.hdfs.HeartbeatsNumOps
  - hadoop.hdfs.ReplaceBlockOpNumOps
  - hadoop.hdfs.VolumeFailures
  - hadoop.hdfs.ReplaceBlockOpAvgTime


"""

import json
import urllib2
import time
import socket
import sys

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from argus_collector.collectors.etc.hdfs_config import *


def Charater(hostname, ip, config_path):
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
        if name == "dfs.namenode.http-address":
            config_ip = value.split(":")[0]
            if config_ip == "0.0.0.0" or config_ip == ip:
                return "NameNode"
            else:
                return "DataNode"


def print_metric(metric, ts, value, tags=""):
    """
    this function is to print record to insert into opentsdb
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
    # print "hadoop.hdfs.{me} {ts} {value} {tags}".format(me=metric, ts=int(ts), value=value,
    #                                      tags=tags)
    print "hadoop.hdfs.%s %d %s %s" % (metric, int(ts), value,
                                       tags)


def get_data(host, port, metric_list, ts, tag):
    for mbean in metric_list.keys():
        try:
            jmx_site = "http://{host}:{port}/jmx?qry={mbean}".format(host=host,
                                                                     port=port, mbean=mbean)
            origin_response = urllib2.urlopen(jmx_site)
            response_content = origin_response.read()
            json_response = json.loads(response_content)['beans']
            useable_content = json_response[0]
            for item in metric_list[mbean]:
                value = useable_content[item]
                print_metric(item, ts, value, tag)
        except IndexError or  urllib2.URLError:
            continue


def main(host, metric_list, tag, hostname):
    sys.stdin.close()
    # sock = socket.socket()
    # real_host = sock.getsockname()
    # print(real_host)
    host = host
    hosttag = "host={hostname} ".format(hostname=hostname)
    tags = "{hosttag}{tag}".format(hosttag=hosttag, tag=tag)
    ts = time.time()
    get_data(host, port, metric_list, ts, tags)


if __name__ == "__main__":
    confdir = hdfs_config_path
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    print(ip)
    if manual_charater == None:
        charater = Charater(hostname, ip, confdir)
    else:
        charater = manual_charater
    if charater == "NameNode":
        metric_list = NameNode_metric_dict
        port = Namenode_jmx_port
        tag = "node=NameNode"
    else:
        metric_list = DataNode_metric_dict
        port = DataNode_jmx_port
        tag = "node=DataNode"
        delkey = "Hadoop:service=DataNode,name=DataNodeActivity-$hostname-50010"
        # effectkey = "Hadoop:service=DataNode,name=DataNodeActivity-{hostname}-50010".format(
        #     hostname=hostname)
        effectkey = "Hadoop:service=DataNode,name=DataNodeActivity-{hostname}-50010".format(
                 hostname="cdh180")
        metric_list[effectkey] = metric_list[delkey]
        del (metric_list[delkey])

    sys.exit(main(host=host, metric_list=metric_list, tag=tag, hostname=hostname))
