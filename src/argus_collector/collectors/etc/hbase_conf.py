# coding=utf8
"""
这个文件是用于配置HBase监控的文件

"""

Property = ['region_file','config_path','host','master_port','manual_charater','region_port']

manual_charater = 'RegionServer'

region_file = '/etc/hbase/conf/regionservers'

config_path = '/etc/hbase/conf/hbase-site.xml'

host = 'localhost'

manual_charater = "region_server" ## 可选为region_server master 或者both，当为None时，采集器自动读取配置文件判断

#master_port = 60010
master_port = 16030

# master_metric = {
#     'Hadoop:service=HBase,name=Master,sub=Server': [

#         # 'tag.liveRegionServers',  #string
#         # 'tag.deadRegionServers',  #string
#         'averageLoad',  #int
#         'numRegionServers',  #int
#         'numDeadRegionServers',  #int

#     ]
# }


# new_master_metric_dict={
#     'Hadoop:service=HBase,name=Master,sub=AssignmentManger':[
#         'ritOldestAge','ritCountOverThreshold','BulkAssign_num_ops',
#         'BulkAssign_min','BulkAssign_max','BulkAssign_mean',
#         'ritCount','Assign_num_ops','Assign_min','Assign_max',
#         'Assign_mean'
#     ],
#     'Hadoop:service=HBase,name=Master,sub=IPC':[
#         'queueSize','numCallsInGeneralQueue','numCallsInReplicationQueue',
#         'numCallsInPriorityQueue','numOpenConnections','numActiveHandler',
#         'numGeneralCallsDropped','numLifoModeSwitches',
#         'exceptions.RegionMovedException','exceptions.multiResponseTooLarge',
#         'authenticationSuccesses','authorizationFailures',
#         'exceptions.RegionTooBusyException','exceptions.FailedSanityCheckException',
#         'exceptions.UnknownScannerException','exceptions.OutOfOrderScannerNextException',
#         'exceptions','ProcessCallTime_num_ops','ProcessCallTime_min',
#         'ProcessCallTime_mean','ProcessCallTime_max','ProcessCallTime_min',
#         'authenticationFallbacks','exceptions.NotServingRegionException',
#         'exceptions.callQueueTooBig','authorizationSuccesses',
#         'exceptions.ScannerResetException','sentBytes','QueueCallTime_num_ops',
#         'QueueCallTime_min','QueueCallTime_max','QueueCallTime_mean',
#         'authenticationFailures'
#     ],
#     'Hadoop:service=HBase,name=Master,sub=Server':[
#         'mergePlanCount','splitPlanCount','averageLoad',
#         'numRegionServers','numDeadRegionServers','clusterRequests'
#     ]
# }

#region_port = 60030
region_port = 16030

# region_server_metric = {
#     'Hadoop:service=HBase,name=RegionServer,sub=Server': [
#         'totalRequestCount',   #int
#         'blockCacheFreeSize',  #int
#         'readRequestCount',    #总读次数 int
#         'writeRequestCount',   #总写次数 int
#         'flushedCellsCount',   # int
#         'flushedCellsSize',    #flush到磁盘大小 int
#         'flushQueueLength',    #  int
#         'blockedRequestCount', #因memstore大于阈值而引发flush的次数 int
#         'slowGetCount',        #请求完成时间超过1000ms的次数 int
#         'storeCount',          #该Region Server管理的store个数 int
#         'mutationsWithoutWALCount',  #int
#         'mutationsWithoutWALSize',  #int
#         'blockCacheHitCount',   #int
#         'blockCacheMissCount',   # int
#     ],
#     'Hadoop:service=HBase,name=RegionServer,sub=IPC': [
#         'numActiveHandler',    #int
#     ],
#     'Hadoop:service=HBase,name=RegionServer,sub=WAL': [
#         'slowAppendCount',  #int
#         'SyncTime_num_ops',   #int
#         'SyncTime_max',       #float
#         'SyncTime_mean',      #float
#         'AppendTime_num_ops',    #int
#         'AppendTime_max',   #float
#         'AppendTime_mean',  #float
#     ],
# }


# new_region_server = {
#     'Hadoop:service=HBase,name=RegionServer,sub=IPC':[
#         'numCallsInGeneralQueue','numCallsInReplicationQueue',
#         'numCallsInPriorityQueue','numActiveHandler',
#         'exceptions.RegionMovedException','exceptions.multiResponseTooLarge',
#         'exceptions.UnknownScannerException','QueueCallTime_num_ops',
#         'QueueCallTime_min','QueueCallTime_max','QueueCallTime_mean',
#         'ProcessCallTime_num_ops','ProcessCallTime_min',
#         'ProcessCallTime_max','ProcessCallTime_mean',
        

#     ],
#     'Hadoop:service=HBase,name=RegionServer,sub=Server':[
#         'regionCount','storeFileCount','storeFileSize',
#         'hlogFileCount','totalRequestCount','readRequestCount',
#         'writeRequestCount','numOpenConnections','numActiveHandler',
#         'flushQueueLength','updatesBlockedTime','compactionQueueLength',
#         'blockCacheHitCount','blockCacheMissCount','blockCacheExpressHitPercent',
#         'percentFilesLocal','mutationsWithoutWALCount','slowGetCount',
#         'Append_num_ops','Append_max','Append_mean','Append_min',
#         'Replay_num_ops','Replay_min','Replay_max','Replay_min',
#         'Mutate_num_ops','Mutate_min','Mutate_max','Mutate_mean',
#         'Get_num_ops','Get_min','Get_max','Get_mean',
#         'Increment_num_ops','Increment_min','Increment_max','Increment_mean'
#     ],
#     'Hadoop:service=HBase,name=JvmMetrics':[
#         'MemNonHeapUsedM','MemNonHeapCommittedM','MemNonHeapMaxM',
#         'MemHeapUsedM','MemHeapCommittedM','MemHeapMaxM','MemMaxM',
#         'GcCountParNew','GcTimeMillisParNew','GcCountConcurrentMarkSweep',
#         'GcTimeMillisConcurrentMarkSweep','GcCount','GcTimeMillis',
#         'ThreadsNew','ThreadsRunnable','ThreadsBlocked','ThreadsWaiting',
#         'ThreadsTimedWaiting','ThreadsTerminated','LogFatal','LogError',
#         'LogWarn','LogInfo'
#     ]
# }

"""
Master 

0.Hadoop:service=HBase,name=Master,sub=AssignmentManger 
数据示例：
{
"name":"Hadoop:service=HBase,name=Master,sub=AssignmentManger",
"modelerType":"Master,sub=AssignmentManger",
"tag.Context":"master",
"tag.Hostname":"workvm",
"ritOldestAge":0,
"ritCountOverThreshold":0,
"BulkAssign_num_ops":1,
"BulkAssign_min":137,
"BulkAssign_max":137,
"BulkAssign_mean":137,
"BulkAssign_25th_percentile":137,
"BulkAssign_median":137,
"BulkAssign_75th_percentile":137,
"BulkAssign_90th_percentile":137,
"BulkAssign_95th_percentile":137,
"BulkAssign_98th_percentile":137,
"BulkAssign_99th_percentile":137,
"BulkAssign_99.9th_percentile":137,
"BulkAssign_TimeRangeCount_0-1":1,
"ritCount":0,
"Assign_num_ops":1,
"Assign_min":470,
"Assign_max":470,
"Assign_mean":470,
"Assign_25th_percentile":470,
"Assign_median":470,
"Assign_75th_percentile":470,
"Assign_90th_percentile":470,
"Assign_95th_percentile":470,
"Assign_98th_percentile":470,
"Assign_99th_percentile":470,
"Assign_99.9th_percentile":470,
"Assign_TimeRangeCount_0-1":1
},

Metric：

hadoop.hbase.Master.ritOldestAge                           # Master管理下的region 状态迁移的最长时间 
hadoop.hbase.Master.ritCountOverThreshold                  # 状态迁移超过阈值（默认为60秒）
hadoop.hbase.Master.BulkAssign_num_ops                     # 
hadoop.hbase.Master.BulkAssign_min
hadoop.hbase.Master.BulkAssign_max
hadoop.hbase.Master.BulkAssign_mean
hadoop.hbase.Master.ritCount                            # 转移状态中的regionserver
hadoop.hbase.Master.Assign_num_ops
hadoop.hbase.Master.Assign_min
hadoop.hbase.Master.Assign_max
hadoop.hbase.Master.Assign_mean

1. Hadoop:service=HBase,name=Master,sub=IPC

数据示例：
{
"name":"Hadoop:service=HBase,name=Master,sub=IPC",
"modelerType":"Master,sub=IPC",
"tag.Context":"master",
"tag.Hostname":"workvm",
"queueSize":0,
"numCallsInGeneralQueue":0,
"numCallsInReplicationQueue":0,
"numCallsInPriorityQueue":0,
"numOpenConnections":1,
"numActiveHandler":0,
"numGeneralCallsDropped":0,
"numLifoModeSwitches":0,
"receivedBytes":1404,
"exceptions.RegionMovedException":0,
"exceptions.multiResponseTooLarge":0,
"authenticationSuccesses":0,
"authorizationFailures":0,
"exceptions.RegionTooBusyException":0,
"exceptions.FailedSanityCheckException":0,
"exceptions.UnknownScannerException":0,
"exceptions.OutOfOrderScannerNextException":0,
"exceptions":0,
"ProcessCallTime_num_ops":6,
"ProcessCallTime_min":1,
"ProcessCallTime_max":202,
"ProcessCallTime_mean":35,
"ProcessCallTime_median":101,
"authenticationFallbacks":0,
"exceptions.NotServingRegionException":0,
"exceptions.callQueueTooBig":0,
"authorizationSuccesses":1,
"exceptions.ScannerResetException":0,
"sentBytes":234,
"QueueCallTime_num_ops":6,
"QueueCallTime_min":0,
"QueueCallTime_max":43,
"QueueCallTime_mean":7,
"authenticationFailures":0
},
Metric

hadoop.hbase.Master.queueSize
hadoop.hbase.Master.numCallsInGeneralQueue
hadoop.hbase.Master.numCallsInReplicationQueue
hadoop.hbase.Master.numCallsInPriorityQueue
hadoop.hbase.Master.numOpenConnections
hadoop.hbase.Master.numActiveHandler
hadoop.hbase.Master.numGeneralCallsDropped
hadoop.hbase.Master.numLifoModeSwitches
hadoop.hbase.Master.receivedBytes":1404,
hadoop.hbase.Master.exceptions.RegionMovedException
hadoop.hbase.Master.exceptions.multiResponseTooLarge
hadoop.hbase.Master.authenticationSuccesses
hadoop.hbase.Master.authorizationFailures
hadoop.hbase.Master.exceptions.RegionTooBusyException
hadoop.hbase.Master.exceptions.FailedSanityCheckException
hadoop.hbase.Master.exceptions.UnknownScannerException
hadoop.hbase.Master.exceptions.OutOfOrderScannerNextException
hadoop.hbase.Master.exceptions
hadoop.hbase.Master.ProcessCallTime_num_ops
hadoop.hbase.Master.ProcessCallTime_min
hadoop.hbase.Master.ProcessCallTime_max
hadoop.hbase.Master.ProcessCallTime_mean
hadoop.hbase.Master.ProcessCallTime_median
hadoop.hbase.Master.authenticationFallbacks
hadoop.hbase.Master.exceptions.NotServingRegionException
hadoop.hbase.Master.exceptions.callQueueTooBig
hadoop.hbase.Master.authorizationSuccesses
hadoop.hbase.Master.exceptions.ScannerResetException
hadoop.hbase.Master.sentBytes":234,
hadoop.hbase.Master.QueueCallTime_num_ops
hadoop.hbase.Master.QueueCallTime_min
hadoop.hbase.Master.QueueCallTime_max
hadoop.hbase.Master.QueueCallTime_mean
hadoop.hbase.Master.authenticationFailures


2. Hadoop:service=HBase,name=Master,sub=Server
数据示例：
{
"name":"Hadoop:service=HBase,name=Master,sub=Server",
"modelerType":"Master,sub=Server",
"tag.liveRegionServers":"ubuntu2,16020,1516261550951",
"tag.deadRegionServers":"",
"tag.zookeeperQuorum":"192.168.232.128:2181",
"tag.serverName":"workvm,16000,1516261522332",
"tag.clusterId":"cdd4999b-8f9f-4501-937f-32b636f62130",
"tag.isActiveMaster":"true",
"tag.Context":"master",
"tag.Hostname":"workvm",
"mergePlanCount":0,
"splitPlanCount":0,
"masterActiveTime":1516261553786,
"masterStartTime":1516261522332,
"averageLoad":2.0,
"numRegionServers":1,
"numDeadRegionServers":0,
"clusterRequests":23
},

hadoop.hbase.Master.mergePlanCount             ###
hadoop.hbase.Master.splitPlanCount             ###
hadoop.hbase.Master.averageLoad                ###平均负载
hadoop.hbase.Master.numRegionServers           ###存活的Region
hadoop.hbase.Master.numDeadRegionServers       ###死去的Region
hadoop.hbase.Master.clusterRequests            ###集群总请求数

RegionServer

0. Hadoop:service=HBase,name=RegionServer,sub=IPC
数据示例：
 {
    "name" : "Hadoop:service=HBase,name=RegionServer,sub=IPC",
    "modelerType" : "RegionServer,sub=IPC",
    "tag.Context" : "regionserver",
    "tag.Hostname" : "ubuntu2",
    "queueSize" : 0,
    "numCallsInGeneralQueue" : 0,
    "numCallsInReplicationQueue" : 0,
    "numCallsInPriorityQueue" : 0,
    "numOpenConnections" : 0,
    "numActiveHandler" : 0,
    "numGeneralCallsDropped" : 0,
    "numLifoModeSwitches" : 0,
    "receivedBytes" : 6927,
    "exceptions.RegionMovedException" : 0,
    "exceptions.multiResponseTooLarge" : 0,
    "authenticationSuccesses" : 0,
    "authorizationFailures" : 0,
    "exceptions.RegionTooBusyException" : 0,
    "exceptions.FailedSanityCheckException" : 0,
    "ResponseSize_num_ops" : 57,
    "ResponseSize_min" : 0,
    "ResponseSize_max" : 0,
    "ResponseSize_mean" : 0,
    "ResponseSize_median" : 0,
    "exceptions.UnknownScannerException" : 0,
    "exceptions.OutOfOrderScannerNextException" : 0,
    "exceptions" : 1,
    "ProcessCallTime_num_ops" : 57,
    "ProcessCallTime_min" : 0,
    "ProcessCallTime_max" : 0,
    "ProcessCallTime_mean" : 0,
    "exceptions.callQueueTooBig" : 0,
    "authorizationSuccesses" : 15,
    "exceptions.ScannerResetException" : 0,
    "RequestSize_num_ops" : 57,
    "RequestSize_min" : 0,
    "RequestSize_max" : 0,
    "RequestSize_mean" : 0,
    "sentBytes" : 10400,
    "QueueCallTime_num_ops" : 57,
    "QueueCallTime_min" : 0,
    "QueueCallTime_max" : 0,
    "QueueCallTime_mean" : 0,
    "authenticationFailures" : 0
  }, 



1. Hadoop:service=HBase,name=RegionServer,sub=Server
数据示例：
{
    "name" : "Hadoop:service=HBase,name=RegionServer,sub=Server",
    "modelerType" : "RegionServer,sub=Server",
    "tag.zookeeperQuorum" : "192.168.232.128:2181",
    "tag.serverName" : "ubuntu2,16020,1516261550951",
    "tag.clusterId" : "cdd4999b-8f9f-4501-937f-32b636f62130",
    "tag.Context" : "regionserver",
    "tag.Hostname" : "ubuntu2",
    "regionCount" : 2,
    "storeCount" : 2,
    "hlogFileCount" : 2,
    "hlogFileSize" : 0,
    "storeFileCount" : 3,
    "memStoreSize" : 832,
    "storeFileSize" : 16557,
    "maxStoreFileAge" : 105671754,
    "minStoreFileAge" : 3558819,
    "avgStoreFileAge" : 71138092,
    "numReferenceFiles" : 0,
    "regionServerStartTime" : 1516261550951,
    "averageRegionSize" : 8694,
    "totalRequestCount" : 61,
    "readRequestCount" : 21,
    "writeRequestCount" : 1,
    "rpcGetRequestCount" : 2,
    "rpcScanRequestCount" : 52,
    "rpcMultiRequestCount" : 1,
    "rpcMutateRequestCount" : 0,
    "checkMutateFailedCount" : 0,
    "checkMutatePassedCount" : 0,
    "storeFileIndexSize" : 1320,
    "staticIndexSize" : 243,
    "staticBloomSize" : 4,
    "mutationsWithoutWALCount" : 0,
    "mutationsWithoutWALSize" : 0,
    "percentFilesLocal" : 100.0,
    "percentFilesLocalSecondaryRegions" : 0.0,
    "splitQueueLength" : 0,
    "compactionQueueLength" : 0,
    "smallCompactionQueueLength" : 0,
    "largeCompactionQueueLength" : 0,
    "compactionQueueLength" : 0,
    "flushQueueLength" : 0,
    "blockCacheFreeSize" : 200930624,
    "blockCacheCount" : 4,
    "blockCacheSize" : 212464,
    "blockCacheHitCount" : 30,
    "blockCacheHitCountPrimary" : 30,
    "blockCacheMissCount" : 4,
    "blockCacheMissCountPrimary" : 4,
    "blockCacheEvictionCount" : 0,
    "blockCacheEvictionCountPrimary" : 0,
    "blockCacheCountHitPercent" : 88.23529481887817,
    "blockCacheExpressHitPercent" : 88.23529481887817,
    "blockCacheFailedInsertionCount" : 0,
    "blockCacheDataMissCount" : 3,
    "blockCacheLeafIndexMissCount" : 0,
    "blockCacheBloomChunkMissCount" : 1,
    "blockCacheMetaMissCount" : 0,
    "blockCacheRootIndexMissCount" : 0,
    "blockCacheIntermediateIndexMissCount" : 0,
    "blockCacheFileInfoMissCount" : 0,
    "blockCacheGeneralBloomMetaMissCount" : 0,
    "blockCacheDeleteFamilyBloomMissCount" : 0,
    "blockCacheTrailerMissCount" : 0,
    "blockCacheDataHitCount" : 29,
    "blockCacheLeafIndexHitCount" : 0,
    "blockCacheBloomChunkHitCount" : 1,
    "blockCacheMetaHitCount" : 0,
    "blockCacheRootIndexHitCount" : 0,
    "blockCacheIntermediateIndexHitCount" : 0,
    "blockCacheFileInfoHitCount" : 0,
    "blockCacheGeneralBloomMetaHitCount" : 0,
    "blockCacheDeleteFamilyBloomHitCount" : 0,
    "blockCacheTrailerHitCount" : 0,
    "updatesBlockedTime" : 0,
    "flushedCellsCount" : 4,
    "compactedCellsCount" : 0,
    "majorCompactedCellsCount" : 0,
    "flushedCellsSize" : 992,
    "compactedCellsSize" : 0,
    "majorCompactedCellsSize" : 0,
    "blockedRequestCount" : 0,
    "MajorCompactionTime_num_ops" : 0,
    "MajorCompactionTime_min" : 0,
    "MajorCompactionTime_max" : 0,
    "MajorCompactionTime_mean" : 0,
    "ScanTime_num_ops" : 18,
    "ScanTime_min" : 0,
    "ScanTime_max" : 0,
    "ScanTime_mean" : 0,
    "Increment_num_ops" : 0,
    "Increment_min" : 0,
    "Increment_max" : 0,
    "Increment_mean" : 0,
    "Delete_num_ops" : 0,
    "Delete_min" : 0,
    "Delete_max" : 0,
    "Delete_mean" : 0,
    "splitRequestCount" : 0,
    "FlushMemstoreSize_num_ops" : 1,
    "FlushMemstoreSize_min" : 0,
    "FlushMemstoreSize_max" : 0,
    "FlushMemstoreSize_mean" : 0,
    "CompactionInputFileCount_num_ops" : 0,
    "CompactionInputFileCount_min" : 0,
    "CompactionInputFileCount_max" : 0,
    "CompactionInputFileCount_mean" : 0,
    "CompactionTime_num_ops" : 0,
    "CompactionTime_min" : 0,
    "CompactionTime_max" : 0,
    "CompactionTime_mean" : 0,
    "Get_num_ops" : 2,
    "Get_min" : 0,
    "Get_max" : 0,
    "Get_mean" : 0,
    "SplitTime_num_ops" : 0,
    "SplitTime_min" : 0,
    "SplitTime_max" : 0,
    "SplitTime_mean" : 0,
    "MajorCompactionOutputSize_num_ops" : 0,
    "MajorCompactionOutputSize_min" : 0,
    "MajorCompactionOutputSize_max" : 0,
    "MajorCompactionOutputSize_mean" : 0,
    "Mutate_num_ops" : 1,
    "Mutate_min" : 0,
    "Mutate_max" : 0,
    "Mutate_mean" : 0,
    "majorCompactedInputBytes" : 0,
    "slowAppendCount" : 0,
    "flushedOutputBytes" : 5254,
    "CompactionOutputFileCount_num_ops" : 0,
    "CompactionOutputFileCount_min" : 0,
    "CompactionOutputFileCount_max" : 0,
    "CompactionOutputFileCount_mean" : 0,
    "slowDeleteCount" : 0,
    "Replay_num_ops" : 0,
    "Replay_min" : 0,
    "Replay_max" : 0,
    "Replay_mean" : 0,
    "FlushTime_num_ops" : 1,
    "FlushTime_min" : 0,
    "FlushTime_max" : 0,
    "FlushTime_mean" : 0,
    "MajorCompactionInputSize_num_ops" : 0,
    "MajorCompactionInputSize_min" : 0,
    "MajorCompactionInputSize_max" : 0,
    "MajorCompactionInputSize_mean" : 0,
    "splitSuccessCount" : 0,
    "CompactionInputSize_num_ops" : 0,
    "CompactionInputSize_min" : 0,
    "CompactionInputSize_max" : 0,
    "CompactionInputSize_mean" : 0,
    "MajorCompactionOutputFileCount_num_ops" : 0,
    "MajorCompactionOutputFileCount_min" : 0,
    "MajorCompactionOutputFileCount_max" : 0,
    "MajorCompactionOutputFileCount_mean" : 0,
    "ScanSize_num_ops" : 18,
    "ScanSize_min" : 0,
    "ScanSize_max" : 0,
    "ScanSize_mean" : 0,
    "slowGetCount" : 0,
    "flushedMemstoreBytes" : 992,
    "CompactionOutputSize_num_ops" : 0,
    "CompactionOutputSize_min" : 0,
    "CompactionOutputSize_max" : 0,
    "CompactionOutputSize_mean" : 0,
    "majorCompactedOutputBytes" : 0,
    "slowPutCount" : 0,
    "slowIncrementCount" : 0,
    "compactedInputBytes" : 0,
    "Append_num_ops" : 0,
    "Append_min" : 0,
    "Append_max" : 0,
    "Append_mean" : 0,



3. Hadoop:service=HBase,name=JvmMetrics 
数据示例：
{
    "name" : "Hadoop:service=HBase,name=JvmMetrics",
    "modelerType" : "JvmMetrics",
    "tag.Context" : "jvm",
    "tag.ProcessName" : "RegionServer",
    "tag.SessionId" : "",
    "tag.Hostname" : "ubuntu2",
    "MemNonHeapUsedM" : 55.78588,
    "MemNonHeapCommittedM" : 56.515625,
    "MemNonHeapMaxM" : -9.536743E-7,
    "MemHeapUsedM" : 24.390244,
    "MemHeapCommittedM" : 33.882812,
    "MemHeapMaxM" : 479.5625,
    "MemMaxM" : 479.5625,
    "GcCountParNew" : 50,
    "GcTimeMillisParNew" : 2301,
    "GcCountConcurrentMarkSweep" : 4,
    "GcTimeMillisConcurrentMarkSweep" : 488,
    "GcCount" : 54,
    "GcTimeMillis" : 2789,
    "ThreadsNew" : 0,
    "ThreadsRunnable" : 19,
    "ThreadsBlocked" : 0,
    "ThreadsWaiting" : 86,
    "ThreadsTimedWaiting" : 21,
    "ThreadsTerminated" : 0,
    "LogFatal" : 0,
    "LogError" : 0,
    "LogWarn" : 0,
    "LogInfo" : 0
  },

Metric:
hadoop.hbase.jvm.
hadoop.hbase.jvm.MemNonHeapUsedM
hadoop.hbase.jvm.MemNonHeapCommittedM
hadoop.hbase.jvm.MemNonHeapMaxM
hadoop.hbase.jvm.MemHeapUsedM
hadoop.hbase.jvm.MemHeapCommittedM
hadoop.hbase.jvm.MemHeapMaxM
hadoop.hbase.jvm.MemMaxM
hadoop.hbase.jvm.GcCountParNew
hadoop.hbase.jvm.GcTimeMillisParNew
hadoop.hbase.jvm.GcCountConcurrentMarkSweep
hadoop.hbase.jvm.GcTimeMillisConcurrentMarkSweep
hadoop.hbase.jvm.GcCount
hadoop.hbase.jvm.GcTimeMillis
hadoop.hbase.jvm.ThreadsNew
hadoop.hbase.jvm.ThreadsRunnable
hadoop.hbase.jvm.ThreadsBlocked
hadoop.hbase.jvm.ThreadsWaiting
hadoop.hbase.jvm.ThreadsTimedWaiting
hadoop.hbase.jvm.ThreadsTerminated
hadoop.hbase.jvm.LogFatal
hadoop.hbase.jvm.LogError 
hadoop.hbase.jvm.LogWarn
hadoop.hbase.jvm.LogInfo

"""