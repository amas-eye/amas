#!/usr/bin/python
# coding=utf-8
"""
这个是用于采集Hbase相关的节点的数据，包括Master和Region_server两个角色

"""

import json
import urllib
import time
import socket
import re
import sys
import os
import copy

# import ptvsd
# ptvsd.settrace(None, ('0.0.0.0', 28000))

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


from argus_collector.collectors.etc.hbase_conf import *
from argus_collector import utils


new_master_metric_dict={
    'Hadoop:service=HBase,name=Master,sub=AssignmentManger':[
        'ritOldestAge','ritCountOverThreshold','BulkAssign_num_ops',
        'BulkAssign_min','BulkAssign_max','BulkAssign_mean',
        'ritCount','Assign_num_ops','Assign_min','Assign_max',
        'Assign_mean','name'
    ],
    'Hadoop:service=HBase,name=Master,sub=IPC':[
        'queueSize','numCallsInGeneralQueue','numCallsInReplicationQueue',
        'numCallsInPriorityQueue','numOpenConnections','numActiveHandler',
        'numGeneralCallsDropped','numLifoModeSwitches',
        'exceptions.RegionMovedException','exceptions.multiResponseTooLarge',
        'authenticationSuccesses','authorizationFailures',
        'exceptions.RegionTooBusyException','exceptions.FailedSanityCheckException',
        'exceptions.UnknownScannerException','exceptions.OutOfOrderScannerNextException',
        'exceptions','ProcessCallTime_num_ops','ProcessCallTime_min',
        'ProcessCallTime_mean','ProcessCallTime_max','ProcessCallTime_min',
        'authenticationFallbacks','exceptions.NotServingRegionException',
        'exceptions.callQueueTooBig','authorizationSuccesses',
        'exceptions.ScannerResetException','sentBytes','QueueCallTime_num_ops',
        'QueueCallTime_min','QueueCallTime_max','QueueCallTime_mean',
        'authenticationFailures','name'
    ],
    'Hadoop:service=HBase,name=Master,sub=Server':[
        'mergePlanCount','splitPlanCount','averageLoad',
        'numRegionServers','numDeadRegionServers','clusterRequests','name'
    ]
}

new_master_list = [
    'Hadoop:service=HBase,name=Master,sub=AssignmentManger',
    'Hadoop:service=HBase,name=Master,sub=IPC',
    'Hadoop:service=HBase,name=Master,sub=Server'
]

new_master_map = {
    'Hadoop:service=HBase,name=Master,sub=AssignmentManger':'MasterAssign',
    'Hadoop:service=HBase,name=Master,sub=IPC':'MasterIPC',
    'Hadoop:service=HBase,name=Master,sub=Server':'Masterbase'
}

new_region_server = {
    'Hadoop:service=HBase,name=RegionServer,sub=IPC':[
        'numCallsInGeneralQueue','numCallsInReplicationQueue',
        'numCallsInPriorityQueue','numActiveHandler',
        'exceptions.RegionMovedException','exceptions.multiResponseTooLarge',
        'exceptions.UnknownScannerException','QueueCallTime_num_ops',
        'QueueCallTime_min','QueueCallTime_max','QueueCallTime_mean',
        'ProcessCallTime_num_ops','ProcessCallTime_min',
        'ProcessCallTime_max','ProcessCallTime_mean','name'
        

    ],
    'Hadoop:service=HBase,name=RegionServer,sub=Server':[
        'regionCount','storeFileCount','storeFileSize',
        'hlogFileCount','totalRequestCount','readRequestCount',
        'writeRequestCount','numOpenConnections','numActiveHandler',
        'flushQueueLength','updatesBlockedTime','compactionQueueLength',
        'blockCacheHitCount','blockCacheMissCount','blockCacheExpressHitPercent',
        'percentFilesLocal','mutationsWithoutWALCount','slowGetCount',
        'Append_num_ops','Append_max','Append_mean','Append_min',
        'Replay_num_ops','Replay_min','Replay_max','Replay_min',
        'Mutate_num_ops','Mutate_min','Mutate_max','Mutate_mean',
        'Get_num_ops','Get_min','Get_max','Get_mean',
        'Increment_num_ops','Increment_min','Increment_max','Increment_mean',
        'name'
    ],
    'Hadoop:service=HBase,name=JvmMetrics':[
        'MemNonHeapUsedM','MemNonHeapCommittedM','MemNonHeapMaxM',
        'MemHeapUsedM','MemHeapCommittedM','MemHeapMaxM','MemMaxM',
        'GcCountParNew','GcTimeMillisParNew','GcCountConcurrentMarkSweep',
        'GcTimeMillisConcurrentMarkSweep','GcCount','GcTimeMillis',
        'ThreadsNew','ThreadsRunnable','ThreadsBlocked','ThreadsWaiting',
        'ThreadsTimedWaiting','ThreadsTerminated','LogFatal','LogError',
        'LogWarn','LogInfo','name'
    ]
}


new_region_list = {
    'Hadoop:service=HBase,name=RegionServer,sub=IPC',
    'Hadoop:service=HBase,name=RegionServer,sub=Server',
    'Hadoop:service=HBase,name=JvmMetrics'
}

new_region_map = {
    'Hadoop:service=HBase,name=RegionServer,sub=IPC':'RSIpc',
    'Hadoop:service=HBase,name=RegionServer,sub=Server':'RSServer',
    'Hadoop:service=HBase,name=JvmMetrics':'jvm'
}

newMaster_metric = 'hadoop.hbase.Master'
newRS_metric = 'hadoop.hbase.RegionServer'


def Charater(hostname, ip, region_conf):
    """
    this function is to findout the charater of server
    :param hostname:
    :param ip:
    :param config_path:
    :return: charater (NameNode or DataNode)
    """
    with open(region_conf,'r') as f:
        Master = True
        for line in f:
            if line == hostname or line == ip:
                Master = False
                break
        if Master:
            Charater = 'master'
        else:
            Charater = 'region_server'
        return Charater

def get_metric(data,base, name_list, name_list_map,Mdict):
    """
    Because of the metric is much more plenty than the other facilities in hadoop
    So this wiil not use exclude to write.
    """
    index_list = []
    item_list = []
    new_item_list = []
    print_string = ''
    ts = int(time.time())
    for single_item in data:
        try:
            if single_item['name'] in name_list: 
               item_list.append(single_item)
        except ValueError:
            print('have no item,check your jmx port confirm the item exist')
            continue
    # print item_list
    for item in item_list:
        Bean = {}
        for metric in Mdict[item['name']]:
            try:
                Bean[metric] = item[metric]
            except KeyError:
                continue
        new_item_list.append(Bean)
    for new_item in new_item_list:
        prefix = name_list_map[new_item['name']]
        new_item.pop('name')
        for key in new_item:
            bm = copy.deepcopy(base)
            bm += ('.'+prefix+'.'+key)
            ptr = '{bm} {t} {v}\n'.format(bm=bm, t=ts, v=new_item[key])
            print_string += ptr
    print print_string

def main():
    ts = time.time()
    TIME_INTERVAL = os.path.basename(os.path.dirname((os.path.abspath(__file__)))).strip()
    confdir = config_path
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    region_conf_file = region_file
    if manual_charater: 
        charater = manual_charater
    else:
        charater = Charater(hostname, ip, region_file)
    if charater == "master":
        metric_dict = new_master_metric_dict
        metric_map = new_master_map
        metric_list = new_master_list
        port = master_port
        base_metric = newMaster_metric
    elif charater == "region_server":
        metric_dict = new_region_server
        metric_map = new_region_map
        metric_list = new_region_list
        port = region_port
        base_metric = newRS_metric
    
    url = 'http://{ip}:{port}/jmx'.format(ip=ip,port=port)
    print url
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    data = data['beans']
    get_metric(data,base_metric,metric_list,metric_map,metric_dict)
    sys.stdout.flush()

if __name__ == "__main__":
    sys.exit(main())