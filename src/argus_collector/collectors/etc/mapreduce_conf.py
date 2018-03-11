#!/usr/bin/env python
# -*- coding: utf-8 -*-
#     Filename @  mapreduce_conf.py
#       Author @  gouhao
#  Create date @  2017-07-26


Property = ['JOBHISTORY_HOST','JOBHITORY_PORT','manual_charater','RESOURCEMANAGER_PORT',
            'NODEMANAGER_PORT','YARN_SITE_CONFIG_PATH','SLAVES_CONFIG_PATH']

JOBHISTORY_HOST = 'localhost'
JOBHITORY_PORT = '19888'

manual_charater = 'RM'   ## charater is three kind RM(resourcemanager)、NM(nodemanager)、standalone

# RESOURCEMANAGER_HOST = 'localhost'

RESOURCEMANAGER_PORT = 8088

# NODEMANAGER_HOST = 'localhost'

NODEMANAGER_PORT = 8042

YARN_SITE_CONFIG_PATH = '/root/hadoop-2.7.3/etc/hadoop/yarn-site.xml'

SLAVES_CONFIG_PATH = '/root/hadoop-2.7.3/etc/hadoop/slaves'

# RESOURCE_MANAGER_METRIC_DICT = {
#     'cluster_metrics':  # GET http://<rm http address:port>/ws/v1/cluster/metrics
#     [
#             'appsSubmitted',  # int
#             'appsCompleted',  # int
#             'appsPending',  # int
#             'appsRunning',  # int
#             'appsFailed',  # int
#             'appsKilled',  # int
#             'reservedMB',  # long
#             'availableMB',  # long
#             'allocatedMB',  # long
#             'totalMB',  # long
#             'reservedVirtualCores',  # long
#             'availableVirtualCores',  # long
#             'allocatedVirtualCores',  # long
#             'totalVirtualCores',  # long
#             'containersAllocated',  # int
#             'containersReserved',  # int
#             'containersPeding',  # int
#             'totalNodes',  # int
#             'activeNodes',  # int
#             'lostNodes',  # int
#             'unhealthyNodes',  # int
#             'decommissionedNodes',  # int
#             'rebootedNodes',  # int
#     ]
# }

# NODEMANAGER_METRIC_DICT = {
#     'node_info':  # GET http://<nm http address:port>/ws/v1/node/info
#     [
#             'totalVmemAllocatedContainersMB',
#             'totalVCoresAllocatedContainers',
#             'totalPmemAllocatedContainersMB',
#     ]
# }


'''
采集的mbeans名称：
0. Cluster
Hadoop:service=ResourceManager,name=ClusterMetrics
数据示例：
"name":"Hadoop:service=ResourceManager,name=ClusterMetrics",
"modelerType":"ClusterMetrics",
"tag.ClusterMetrics":"ResourceManager",
"tag.Context":"yarn",
"tag.Hostname":"workvm",
"NumActiveNMs":1,
"NumDecommissionedNMs":0,
"NumLostNMs":0,
"NumUnhealthyNMs":0,
"NumRebootedNMs":0,
"AMLaunchDelayNumOps":0,
"AMLaunchDelayAvgTime":0.0,
"AMRegisterDelayNumOps":0,
"AMRegisterDelayAvgTime":0.0

Metric为：
hadoop.mapreduce.RM.cluster.NumActiveNMs  ## 存活的NodeManager数量
hadoop.mapreduce.RM.cluster.NumDecommissionedNMs ## 被删除的NodeManager数量
hadoop.mapreduce.RM.cluster.NumLostNMs    ## 死去的NodeManager数量
hadoop.mapreduce.RM.cluster.NumUnhealthyNMs ## 不健康的NodeManager数量
hadoop.mapreduce.RM.cluster.NumRebootedNMs  ## 重启的NodeManager数量
hadoop.mapreduce.RM.cluster.AMLaunchDelayNumOps ## 
hadoop.mapreduce.RM.cluster.AMLaunchDelayAvgTime ##
hadoop.mapreduce.RM.cluster.AMRegisterDelayNumOps ##
hadoop.mapreduce.RM.cluster.AMRegisterDelayAvgTime ## 

1. ResourceManager,name=RpcActivityForPort8030(8030可以修改为其他端口,可能有多个port) 
{
"name":"Hadoop:service=ResourceManager,name=RpcActivityForPort8030",  
"modelerType":"RpcActivityForPort8030",
"tag.port":"8030",
"tag.Context":"rpc",
"tag.NumOpenConnectionsPerUser":"{}",
"tag.Hostname":"workvm",
"ReceivedBytes":0,
"SentBytes":0,
"RpcQueueTimeNumOps":0,
"RpcQueueTimeAvgTime":0.0,
"RpcProcessingTimeNumOps":0,
"RpcProcessingTimeAvgTime":0.0,
"RpcAuthenticationFailures":0,
"RpcAuthenticationSuccesses":0,
"RpcAuthorizationFailures":0,
"RpcAuthorizationSuccesses":0,
"RpcSlowCalls":0,
"RpcClientBackoff":0,
"NumOpenConnections":0,
"CallQueueLength":0,
"NumDroppedConnections":0
},

这里是通用的rpc状态可以在metric中查找
Metric
hadoop.mapreduce.RM.RpcQueueTimeNumOps
hadoop.mapreduce.RM.RpcQueueTimeAvgTime
hadoop.mapreduce.RM.RpcProcessingTimeNumOps
hadoop.mapreduce.RM.RpcProcessingTimeAvgTime
hadoop.mapreduce.RM.RpcAuthenticationFailures
hadoop.mapreduce.RM.RpcAuthenticationSuccesses
hadoop.mapreduce.RM.RpcAuthorizationFailures
hadoop.mapreduce.RM.RpcAuthorizationSuccesses
hadoop.mapreduce.RM.RpcSlowCalls
hadoop.mapreduce.RM.RpcClientBackoff
hadoop.mapreduce.RM.NumOpenConnections
hadoop.mapreduce.RM.CallQueueLength
hadoop.mapreduce.RM.NumDroppedConnections

2. Hadoop:service=ResourceManager,name=QueueMetrics,q0=root,q1=default
数据示例：
"name":"Hadoop:service=ResourceManager,name=QueueMetrics,q0=root,q1=default",
"modelerType":"QueueMetrics,q0=root,q1=default",
"tag.Queue":"root.default",
"tag.Context":"yarn",
"tag.Hostname":"workvm",
"running_0":0,
"running_60":0,
"running_300":0,
"running_1440":0,
"AppsSubmitted":0,
"AppsRunning":0,
"AppsPending":0,
"AppsCompleted":0,
"AppsKilled":0,
"AppsFailed":0,
"AllocatedMB":0,
"AllocatedVCores":0,
"AllocatedContainers":0,
"AggregateContainersAllocated":0,
"AggregateNodeLocalContainersAllocated":0,
"AggregateRackLocalContainersAllocated":0,
"AggregateOffSwitchContainersAllocated":0,
"AggregateContainersReleased":0,
"AvailableMB":8192,
"AvailableVCores":8,
"PendingMB":0,
"PendingVCores":0,
"PendingContainers":0,
"ReservedMB":0,
"ReservedVCores":0,
"ReservedContainers":0,
"ActiveUsers":0,
"ActiveApplications":0

Metric

hadoop.mapreduce.RM.running_0    ## 运行时间小于60分钟的app
hadoop.mapreduce.RM.running_60   ## 运行时间60-300分钟的app
hadoop.mapreduce.RM.running_300  ## 运行时间300-1440分钟的app
hadoop.mapreduce.RM.running_1440 ## 运行时间1440分钟的app
hadoop.mapreduce.RM.AppsSubmitted ## 总共提交的数量
hadoop.mapreduce.RM.AppsRunning   ## 正在运行的app数量
hadoop.mapreduce.RM.AppsPending   ## 等待运行的app数量
hadoop.mapreduce.RM.AppsCompleted ## 完成的app的数量
hadoop.mapreduce.RM.AppsKilled    ## 被杀死的app的数量
hadoop.mapreduce.RM.AppsFailed    ## 运行失败的app的数量
hadoop.mapreduce.RM.AllocatedMB   ## 分配的内存（以MB为单位）
hadoop.mapreduce.RM.AllocatedVCores  ## 
hadoop.mapreduce.RM.AllocatedContainers
hadoop.mapreduce.RM.AggregateContainersAllocated
hadoop.mapreduce.RM.AggregateNodeLocalContainersAllocated
hadoop.mapreduce.RM.AggregateRackLocalContainersAllocated
hadoop.mapreduce.RM.AggregateOffSwitchContainersAllocated
hadoop.mapreduce.RM.AggregateContainersReleased
hadoop.mapreduce.RM.AvailableMB   ## 可用内存（单位为MB）
hadoop.mapreduce.RM.AvailableVCores ## 可用虚拟和
hadoop.mapreduce.RM.PendingMB
hadoop.mapreduce.RM.PendingVCores
hadoop.mapreduce.RM.PendingContainers
hadoop.mapreduce.RM.ReservedMB    ## 现在的剩余内存
hadoop.mapreduce.RM.ReservedVCores  ## 
hadoop.mapreduce.RM.ReservedContainers
hadoop.mapreduce.RM.ActiveUsers     ## 现在的活跃用户数
hadoop.mapreduce.RM.ActiveApplications  ## 活跃的应用数


4.name":"Hadoop:service=ResourceManager,name=RpcDetailedActivityForPort8031

数据示例：
{
"name":"Hadoop:service=ResourceManager,name=RpcDetailedActivityForPort8031",
"modelerType":"RpcDetailedActivityForPort8031",
"tag.port":"8031",
"tag.Context":"rpcdetailed",
"tag.Hostname":"workvm",
"NodeHeartbeatNumOps":16418,
"NodeHeartbeatAvgTime":0.3931660372761603,
"RegisterNodeManagerNumOps":1,
"RegisterNodeManagerAvgTime":12.0
},

Metric
hadoop.mapreduce.RM.NodeHeartbeatNumOps           ## NodeManager心跳个数（活跃数）
hadoop.mapreduce.RM.NodeHeartbeatAvgTime          ## NodeManager心跳时间
hadoop.mapreduce.RM.RegisterNodeManagerNumOps     ## 注册的NodeManager数量
hadoop.mapreduce.RM.RegisterNodeManagerAvgTime    ## 注册平均时间


【NodeManager】
0. Hadoop:service=NodeManager,name=NodeManagerMetrics

数据示例：
{
"name":"Hadoop:service=NodeManager,name=NodeManagerMetrics",
"modelerType":"NodeManagerMetrics",
"tag.Context":"yarn",
"tag.Hostname":"ubuntu2",
"ContainersLaunched":0,
"ContainersCompleted":0,
"ContainersFailed":0,
"ContainersKilled":0,
"ContainersIniting":0,
"ContainersRunning":0,
"AllocatedGB":0,
"AllocatedContainers":0,
"AvailableGB":8,
"AllocatedVCores":0,
"AvailableVCores":8,
"ContainerLaunchDurationNumOps":0,
"ContainerLaunchDurationAvgTime":0.0
},

Metric
hadoop.mapreduce.NM.ContainersLaunched  ## 
hadoop.mapreduce.NM.ContainersCompleted ## 运行成功的容器（总数）
hadoop.mapreduce.NM.ContainersFailed   ## 运行失败的容器（总数）
hadoop.mapreduce.NM.ContainersKilled   ## 被杀掉的容器（总数）
hadoop.mapreduce.NM.ContainersIniting  ## 正在初始化的容器
hadoop.mapreduce.NM.ContainersRunning  ## 
hadoop.mapreduce.NM.AllocatedGB        ## 内存使用量
hadoop.mapreduce.NM.AllocatedContainers ## 
hadoop.mapreduce.NM.AvailableGB         ## 可用的内存量
hadoop.mapreduce.NM.AllocatedVCores     ## 正在使用的核心
hadoop.mapreduce.NM.AvailableVCores     ## 可用的核心
hadoop.mapreduce.NM.ContainerLaunchDurationNumOps 
hadoop.mapreduce.NM.ContainerLaunchDurationAvgTime


1. jvm
{
    "name" : "Hadoop:service=NodeManager,name=JvmMetrics",
    "modelerType" : "JvmMetrics",
    "tag.Context" : "jvm",
    "tag.ProcessName" : "NodeManager",
    "tag.SessionId" : null,
    "tag.Hostname" : "ubuntu2",
    "MemNonHeapUsedM" : 46.704758,
    "MemNonHeapCommittedM" : 48.125,
    "MemNonHeapMaxM" : -9.536743E-7,
    "MemHeapUsedM" : 128.9769,
    "MemHeapCommittedM" : 153.0,
    "MemHeapMaxM" : 889.0,
    "MemMaxM" : 889.0,
    "GcCount" : 11,
    "GcTimeMillis" : 1595,
    "ThreadsNew" : 0,
    "ThreadsRunnable" : 15,
    "ThreadsBlocked" : 0,
    "ThreadsWaiting" : 11,
    "ThreadsTimedWaiting" : 37,
    "ThreadsTerminated" : 0,
    "LogFatal" : 0,
    "LogError" : 0,
    "LogWarn" : 2,
    "LogInfo" : 65
  }

Metric

hadoop.mapreduce.NM.GcCount             ##总gc数
hadoop.mapreduce.NM.GcTimeMillis        ##总gc时间（毫秒）
hadoop.mapreduce.NM.ThreadsNew          ##当前新建线程数
hadoop.mapreduce.NM.ThreadsRunnable     ##当前可运行线程数
hadoop.mapreduce.NM.ThreadsBlocked      ##当前阻塞线程数
hadoop.mapreduce.NM.ThreadsWaiting      ##当前等待线程数
hadoop.mapreduce.NM.ThreadsTimedWaiting ##当前定时等待线程
hadoop.mapreduce.NM.ThreadsTerminated   ##当前终结线程数
hadoop.mapreduce.NM.LogFatal            ##严重错误总记录数
hadoop.mapreduce.NM.LogError            ##错误总记录数


'''
