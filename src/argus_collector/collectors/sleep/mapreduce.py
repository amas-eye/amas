#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Monitor the mapreduce  metrics both resourcemanger and nodemanager.
See more details in argus/doc/Metrics.md, ../etc/mapreduce_conf.py

node = ResoucreManager
    hadoop.mapreduce.appsSubmitted
    hadoop.mapreduce.appsCompleted
    hadoop.mapreduce.appsPending
    hadoop.mapreduce.appsRunning
    hadoop.mapreduce.appsFailed
    hadoop.mapreduce.appsKilled
    hadoop.mapreduce.reservedMB
    hadoop.mapreduce.availableMB
    hadoop.mapreduce.allocatedMB
    hadoop.mapreduce.totalMB
    hadoop.mapreduce.reservedVirtualCore
    hadoop.mapreduce.availableVirtualCores
    hadoop.mapreduce.allocatedVirtualCores
    hadoop.mapreduce.totalVirtualCores
    hadoop.mapreduce.containersAllocated
    hadoop.mapreduce.containersReserve
    hadoop.mapreduce.containersPending
    hadoop.mapreduce.totalNodes
    hadoop.mapreduce.activeNodes
    hadoop.mapreduce.lostNodes
    hadoop.mapreduce.unhealthyodes
    hadoop.mapreduce.decommissionedNodes
    hadoop.mapreduce.rebootedNodes
node = NodeManager
    hadoop.mapreduce.totalVmemAllocatedContainersMB
    hadoop.mapreduce.totalVCoresAllocatedContainers
    hadoop.mapreduce.totalPmemAllocatedContainersMB
"""

import json
import urllib2
import time
import socket


try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from argus_collector.collectors.etc.mapreduce_conf import *


def get_rm_data(host, port, timestamp):
    """
    Get the Resource Manager metrics
    """
    url = "http://{host}:{port}/ws/v1/cluster/metrics".format(host=host, port=port)
    origin_response = urllib2.urlopen(url)
    response_content = origin_response.read()
    cluster_dict = json.loads(response_content)
    for key, value in cluster_dict["cluster_metrics"].iteritems():
        if key in RESOURCE_MANAGER_METRIC_DICT["cluster_metrics"]:
            metric_name = "hadoop.mapreduce.%s" % key
            print_metric(metric_name, timestamp, value, tag="node=ResourceManager")


def get_nm_data(host, port, timestamp):
    """
    Get the Node manager metrics
    """
    url = "http://{host}:{port}/ws/v1/node/info".format(host=host, port=port)
    origin_response = urllib2.urlopen(url)
    response_content = origin_response.read()
    node_info_dict = json.loads(response_content)
    for i in NODEMANAGER_METRIC_DICT["node_info"]:
        if i in node_info_dict[u"nodeInfo"].keys():
            metric_name = "hadoop.mapreduce.%s" % i
            value = node_info_dict["nodeInfo"][i]
            print_metric(metric_name, timestamp, value, tag="node=NodeManager")


def figure_out_identity():
    """
    Figure out the host's identity, RM or NM.
    """
    hostname = socket.gethostname()
    with open(SLAVES_CONFIG_PATH) as f:
        if hostname + "\n" in f.readlines():
            return "NodeManager"
    tree = ET.parse(YARN_SITE_CONFIG_PATH)
    root = tree.getroot()
    title = root.findall("property")
    for item in title:
        name = item.find("name").text
        value = item.find("value").text
        if name == "yarn.resourcemanager.hostname" and value == hostname:
            return "ResourceManager"


def print_metric(metric, timestamp, value, tag=""):
    """
    Format the metric output.
    """
    print "%s %d %s %s" % (metric, int(timestamp), value, tag)


def main():
    node_id = figure_out_identity()
    if node_id == "ResourceManager":
        get_rm_data(RESOURCEMANAGER_HOST, RESOURCEMANAGER_PORT, int(time.time()))
    if node_id == "NodeManager":
        get_nm_data(NODEMANAGER_HOST, NODEMANAGER_PORT, int(time.time()))

if __name__ == "__main__":
    main()
