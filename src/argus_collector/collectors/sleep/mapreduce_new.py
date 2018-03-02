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

from argus_collector.collectors.etc.mapreduce_conf import *


RM_list = [
    'Hadoop:service=ResourceManager,name=ClusterMetrics',
    'Hadoop:service=ResourceManager,name=RpcActivityForPort$',
    'Hadoop:service=ResourceManager,name=QueueMetrics,q0=root,q1=default',
    'Hadoop:service=ResourceManager,name=JvmMetrics'
]

RM_list_map = {
    'Hadoop:service=ResourceManager,name=ClusterMetrics':'Cluster',
    'Hadoop:service=ResourceManager,name=QueueMetrics,q0=root,q1=default':'QueueMetric',
    'Hadoop:service=ResourceManager,name=JvmMetrics':'jvm',
    'Hadoop:service=ResourceManager,name=RpcActivityForPort$':'rpc'
}

NM_list = [
    'Hadoop:service=NodeManager,name=NodeManagerMetrics',
    'Hadoop:service=NodeManager,name=JvmMetrics'
]

NM_list_map = {
    'Hadoop:service=NodeManager,name=NodeManagerMetrics':'NMMetric',
    'Hadoop:service=NodeManager,name=JvmMetrics':'jvm',
}

RM_base_metric = 'hadoop.mapreduce.RM'
NM_base_metric = 'hadoop.mapreduce.NM'

exclude_tag = [
    'modelerType', 'tag.ProcessName', 'tag.SessionId', 'tag.Context',
    'tag.Hostname','TopUserOpCounts','tag.Queue','tag.port',
    'tag.NumOpenConnectionsPerUser','tag.ClusterMetrics'
]

rpc_config_items = [
    'yarn.resourcemanager.resource-tracker.address',
    'yarn.resourcemanager.admin.address',
    'yarn.resourcemanager.address'
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
    rpc_ports = []
    charater = ''
    print 'title\n'
    print title
    for item in title:
        name = item.find('name').text
        value = item.find('value').text
        print 'name is {n}\n'.format(n=name)
        print 'name type is {n}\n'.format(n=type(name))
        print 'value is {v}\n'.format(v=value)
        if name in rpc_config_items:
            value_list = value.split(":")
            config_ip = value_list[0]
            config_port = value_list[1]
            if config_ip == hostname or config_ip == ip:
                rpc_ports.append(config_port)
        elif name == 'yarn.resourcemanager.hostname':
            value_list = value.split(":")
            config_ip = value_list[0]
            print 'config ip is {cip}'.format(cip=config_ip)
            if config_ip == hostname or config_ip == ip:
                charater = 'RM'
            else:
                charater = 'NM'
    # print "charater is"
    # print charater
    return (charater,rpc_ports)

def get_metric(data, exclude, base, name_list, name_list_map):
    item_list = []
    print_string = ''
    ts = int(time.time())
    for single_item in data:
        try:
            if single_item['name'] in name_list:
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
        name = new_item['name']
        new_item.pop('name')
        print "prefix is {p}".format(p=prefix)
        prefix_in_rpc = False
        if 'Rpc' in name:
            prefix_in_rpc = True
            this_port = name.split('Port')[1]
            port_tag = 'port={p}'.format(p=this_port)
        for key in new_item:
            bm = copy.deepcopy(base)
            bm += ('.'+prefix+'.'+key)
            if prefix_in_rpc:
                ptr = '{bm} {t} {v} {tag}\n'.format(bm=bm, t=ts, v=new_item[key], tag=port_tag)
            else:
                ptr = '{bm} {t} {v}\n'.format(bm=bm, t=ts, v=new_item[key])
            print_string += ptr
    print print_string

def replace_rpc_metric(namelist,namemap,rpc_list):
    origin_metric = copy.deepcopy(namelist[1])
    value = namemap[origin_metric]
    for port in rpc_list:
        new_metric = copy.deepcopy(origin_metric)
        new_metric = new_metric.replace('$',port)
        namemap[new_metric] = value
        namelist.append(new_metric)
    return (namelist,namemap)


if __name__ == '__main__':
    # for normal use
    # hostname = socket.gethostname()
    # ip = socket.gethostbyname(hostname)

    # for debug use
    ip = '192.168.232.128'
    hostname = socket.gethostname()
    port = None
    use_manual_charater = False
    if manual_charater:
        charater = manual_charater
        use_manual_charater = True
    else:
        charater, rpc_ports = Charater(hostname, ip, YARN_SITE_CONFIG_PATH)
    print charater
    if charater == 'RM':
        url = 'http://{ip}:{port}/jmx'.format(ip=ip,port=RESOURCEMANAGER_PORT)
        base_metric = RM_base_metric
        namelist = RM_list
        name_list_map = RM_list_map
        if use_manual_charater:
            charater_no_use,rpc_ports = Charater(hostname,ip,YARN_SITE_CONFIG_PATH)
        namelist,name_list_map = replace_rpc_metric(namelist,name_list_map,rpc_ports)
    elif charater == 'NM':
        url = 'http://{ip}:{port}/jmx'.format(ip=ip,port=NODEMANAGER_PORT)
        base_metric = NM_base_metric
        namelist = NM_list
        name_list_map = NM_list_map
    ##TODO this part is for standalone
    # else:
    #     urls = []
    #     url0 = 'http://{ip}:{port}/jmx'.format(ip=ip,port=RESOURCEMANAGER_PORT)
    #     url1 = 'http://{ip}:{port}/jmx'.format(ip=ip, port=NODEMANAGER_PORT)
    #     urls.append(url0)
    #     urls.append(url1)

    print namelist
    print name_list_map
    response = urllib.urlopen(url)
    origin_data = response.read()
    json_data = json.loads(origin_data,'utf-8')
    data = json_data['beans']
    get_metric(data, exclude_tag, base_metric,namelist,name_list_map)
