#!/usr/bin/env python
# coding =utf-8
import time
import json
import copy
import socket
import urllib
import json

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from argus_collector.collectors.etc.hdfs_config import *


DataNode_list = [
    'Hadoop:service=DataNode,name=JvmMetrics',
    'Hadoop:service=DataNode,name=DataNodeActivity-hostname-50010'
]

DataNode_list_map = {
    'Hadoop:service=DataNode,name=JvmMetrics':'jvm',
    'Hadoop:service=DataNode,name=DataNodeActivity-hostname-50010':'Activity'
}

NameNode_list = [
    'Hadoop:service=NameNode,name=NameNodeActivity',
    'Hadoop:service=NameNode,name=FSNamesystemState',
    'Hadoop:service=NameNode,name=JvmMetrics'
]

NameNode_list_map = {
    'Hadoop:service=NameNode,name=NameNodeActivity':'Activity',
    'Hadoop:service=NameNode,name=FSNamesystemState':'FSState',
    'Hadoop:service=NameNode,name=JvmMetrics':'jvm'  
}

NameNode_base_metric = 'hadoop.hdfs.NameNode'
DataNode_base_metric = 'hadoop.hdfs.DataNode'

exclude_tag = [
    'modelerType', 'tag.ProcessName', 'tag.SessionId', 'tag.Context',
    'tag.Hostname','TopUserOpCounts'
]

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
            value_list = value.split(":")
            config_ip = value_list[0]
            config_port = value_list[1]
            if config_ip == "0.0.0.0" or config_ip == ip or hostname == config_ip:
                return ("NameNode",config_port)
            else:
                return ("DataNode",None)

def get_metric(data, exclude, base, name_list, name_list_map):
    index_list = []
    item_list = []
    print_string = ''
    ts = int(time.time())
    for single_item in data:
        try:
            # print(name_item)
            # name_index = data.index({'name': name_item})
            if single_item['name'] in name_list: 
            # print(name_index)
               item_list.append(single_item)
        except ValueError:
            print('have no item,check your jmx port confirm the item exist')
            continue
    print item_list
    for item in item_list:
        for exclude_key in exclude:
            try:
                item.pop(exclude_key)
            except KeyError:
                continue
    for new_item in item_list:
        prefix = name_list_map[new_item['name']]
        new_item.pop('name')
        for key in new_item:
            bm = copy.deepcopy(base)
            bm += ('.'+prefix+'.'+key)
            ptr = '{bm} {t} {v}\n'.format(bm=bm, t=ts, v=new_item[key])
            print_string += ptr
    print print_string


if __name__ == '__main__':
    # hostname = socket.gethostname()
    # ip = socket.gethostbyname(hostname)
    # for debug use
    ip = '192.168.232.129'
    hostname = socket.gethostname()
    port = None
    if manual_charater:
        charater = manual_charater
    else:
        charater_tuple = Charater(hostname,ip,hdfs_config_path)
        charater = charater_tuple[0]
        port = charater_tuple[1]
    if charater == 'NameNode':
        if port:
            url = 'http://{ip}:{port}/jmx'.format(ip=ip,port=port)
        else:
            url = 'http://{ip}:{port}/jmx'.format(ip=ip,port=NameNode_jmx_port)
        base_metric = NameNode_base_metric
        namelist = NameNode_list
        name_list_map = NameNode_list_map
    else:
        url = 'http://{ip}:{port}/jmx'.format(ip=ip,port=DataNode_jmx_port)
        base_metric = DataNode_base_metric
        namelist = DataNode_list
        name_list_map = DataNode_list_map
        origin_metric = namelist[1]
        hostname_metric = copy.deepcopy(namelist[1])
        hostname_metric = hostname_metric.replace('hostname',hostname)
        namelist[1] = hostname_metric
        name_list_map[hostname_metric] = name_list_map[origin_metric]

    # print namelist
    response = urllib.urlopen(url)
    origin_data = response.read()
    json_data = json.loads(origin_data,'utf-8')
    data = json_data['beans']
    get_metric(data, exclude_tag, base_metric,namelist,name_list_map)
