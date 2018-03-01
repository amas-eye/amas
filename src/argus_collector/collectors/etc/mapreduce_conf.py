#!/usr/bin/env python
# -*- coding: utf-8 -*-
#     Filename @  mapreduce_conf.py
#       Author @  gouhao
#  Create date @  2017-07-26

JOBHISTORY_HOST = 'localhost'
JOBHITORY_PORT = '19888'

RESOURCEMANAGER_HOST = 'localhost'

RESOURCEMANAGER_PORT = 8088

NODEMANAGER_HOST = 'localhost'

NODEMANAGER_PORT = 8042

YARN_SITE_CONFIG_PATH = '/root/hadoop-2.7.3/etc/hadoop/yarn-site.xml'

SLAVES_CONFIG_PATH = '/root/hadoop-2.7.3/etc/hadoop/slaves'

RESOURCE_MANAGER_METRIC_DICT = {
    'cluster_metrics':  # GET http://<rm http address:port>/ws/v1/cluster/metrics
    [
            'appsSubmitted',  # int
            'appsCompleted',  # int
            'appsPending',  # int
            'appsRunning',  # int
            'appsFailed',  # int
            'appsKilled',  # int
            'reservedMB',  # long
            'availableMB',  # long
            'allocatedMB',  # long
            'totalMB',  # long
            'reservedVirtualCores',  # long
            'availableVirtualCores',  # long
            'allocatedVirtualCores',  # long
            'totalVirtualCores',  # long
            'containersAllocated',  # int
            'containersReserved',  # int
            'containersPeding',  # int
            'totalNodes',  # int
            'activeNodes',  # int
            'lostNodes',  # int
            'unhealthyNodes',  # int
            'decommissionedNodes',  # int
            'rebootedNodes',  # int
    ]
}

NODEMANAGER_METRIC_DICT = {
    'node_info':  # GET http://<nm http address:port>/ws/v1/node/info
    [
            'totalVmemAllocatedContainersMB',
            'totalVCoresAllocatedContainers',
            'totalPmemAllocatedContainersMB',
    ]
}
