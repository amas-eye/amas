# coding=utf8

"""
这个文件是用于配置HDFS采集器的配置文件

"""

Property = ['NameNode_jmx_port','manual_charater','hdfs_config_path','DataNode_jmx_port','host']

NameNode_jmx_port = 50070     ## 默认端口为50070,如果不是用此端口，可以进行配置

manual_charater = "DataNode"  ## 可以选择为DataNode、NameNode、None(使用程序自动读取角色)
# manual_charater = "NameNode"  ## 可以选择为DataNode、NameNode、None(使用程序自动读取角色)

hdfs_config_path = '/etc/hadoop/conf/hdfs-site.xml'  ## 需要使用绝对路径进行写入

# NameNode_metric_dict = {

#     'Hadoop:service=NameNode,name=FSNamesystem': [
#         'CorruptBlocks',      #int
#         'CapacityRemainingGB',    #int
#         'Snapshots',   #int
#         'MissingBlocks',   #int
#     ],
#     'Hadoop:service=NameNode,name=FSNamesystemState': [
#         'VolumeFailuresTotal', #int
#         'NumLiveDataNodes', #int
#         'NumDeadDataNodes', #int
#         'NumStaleDataNodes', #int
#         'NumStaleStorages',  #int
#     ]
#     'Hadoop:service=NameNode,name=JvmMetrics':{
#         'MemNonHeapUsedM',
#         'GcCount',
#         'GcTimeMillis',
#         '',
#         'ThreadsWaiting',
#     }
# }


DataNode_jmx_port = 50075

# DataNode_metric_dict = {
#     'Hadoop:service=DataNode,name=DataNodeActivity-$hostname-50010': [
#         'BlockVerificationFailures', #int
#         'BlockReportsAvgTime',  #float
#         'BlockReportsNumOps',  #int
#         'HeartbeatsAvgTime',   #float
#         'HeartbeatsNumOps',    #int
#         'DatanodeNetworkErrors', #int
#         'VolumeFailures',  #int
#         'ReplaceBlockOpNumOps',  #int
#         'ReplaceBlockOpAvgTime',  #float

#     ],

# }

# host = 'localhost'
host = '192.168.0.180' ##被采集机器的ip（本机的ip）

'''
0. JVM_metric
hadoop.hdfs.namenode.NM.GcCount             ##总gc数
hadoop.hdfs.namenode.NM.GcTimeMillis        ##总gc时间（毫秒）
hadoop.hdfs.namenode.NM.ThreadsNew          ##当前新建线程数
hadoop.hdfs.namenode.NM.ThreadsRunnable     ##当前可运行线程数
hadoop.hdfs.namenode.NM.ThreadsBlocked      ##当前阻塞线程数
hadoop.hdfs.namenode.NM.ThreadsWaiting      ##当前等待线程数
hadoop.hdfs.namenode.NM.ThreadsTimedWaiting ##当前定时等待线程
hadoop.hdfs.namenode.NM.ThreadsTerminated   ##当前终结线程数
hadoop.hdfs.namenode.NM.LogFatal            ##严重错误总记录数
hadoop.hdfs.namenode.NM.LogError            ##错误总记录数



1. Hadoop:service=NameNode,name=NameNodeActivity
数据示例：

"name":"Hadoop:service=NameNode,name=NameNodeActivity",
"modelerType":"NameNodeActivity",
"tag.ProcessName":"NameNode",
"tag.SessionId":null,
"tag.Context":"dfs",
"tag.Hostname":"cdhmaster",
"CreateFileOps":3288,
"FilesCreated":5480,
"FilesAppended":0,
"GetBlockLocations":21017,
"FilesRenamed":713,
"GetListingOps":15271,
"DeleteFileOps":3317,
"FilesDeleted":3317,
"FileInfoOps":23258,
"AddBlockOps":1683,
"GetAdditionalDatanodeOps":0,
"CreateSymlinkOps":0,
"GetLinkTargetOps":0,
"FilesInGetListingOps":136046,
"AllowSnapshotOps":0,
"DisallowSnapshotOps":0,
"CreateSnapshotOps":0,
"DeleteSnapshotOps":0,
"RenameSnapshotOps":0,
"ListSnapshottableDirOps":0,
"SnapshotDiffReportOps":0,
"BlockReceivedAndDeletedOps":3396,
"StorageBlockReportOps":11,
"BlockOpsQueued":1,
"BlockOpsBatched":23,
"TransactionsNumOps":20291,
"TransactionsAvgTime":0.0,
"SyncsNumOps":15884,
"SyncsAvgTime":15.5,
"TransactionsBatchedInSync":2575906,
"BlockReportNumOps":11,
"BlockReportAvgTime":1.0,
"CacheReportNumOps":8858,
"CacheReportAvgTime":0.0,
"SafeModeTime":3463169,
"FsImageLoadTime":3991,
"GetEditNumOps":29,
"GetEditAvgTime":0.0,
"GetImageNumOps":1,
"GetImageAvgTime":62.0,
"PutImageNumOps":29,
"PutImageAvgTime":50.0,
"TotalFileOps":68547
},

2. Hadoop:service=NameNode,name=FSNamesystemState
{
"name":"Hadoop:service=NameNode,name=FSNamesystemState",
"modelerType":"org.apache.hadoop.hdfs.server.namenode.FSNamesystem",
"BlocksTotal":3406,
"UnderReplicatedBlocks":3403,
"CapacityTotal":101955665920,
"CapacityUsed":1455247360,
"CapacityRemaining":62426406912,
"TotalLoad":3,
"SnapshotStats":"{\"SnapshottableDirectories\":0,\"Snapshots\":0}",
"NumEncryptionZones":0,
"FsLockQueueLength":0,
"MaxObjects":0,
"FilesTotal":7937,
"PendingReplicationBlocks":0,
"ScheduledReplicationBlocks":0,
"PendingDeletionBlocks":0,
"BlockDeletionStartTime":1516065448318,
"FSState":"Operational",
"NumLiveDataNodes":2,
"NumDeadDataNodes":0,
"NumDecomLiveDataNodes":0,
"NumDecomDeadDataNodes":0,
"VolumeFailuresTotal":0,
"EstimatedCapacityLostTotal":0,
"NumDecommissioningDataNodes":0,
"NumStaleDataNodes":0,
"NumStaleStorages":0,
"TopUserOpCounts":"{\"timestamp\":\"2018-01-17T14:47:17+0800\",\"windows\":[{\"ops\":[{\"opType\":\"listCachePools\",\"topUsers\":[{\"user\":\"impala\",\"count\":1},{\"user\":\"hdfs\",\"count\":1}],\"totalCount\":2},{\"opType\":\"listStatus\",\"topUsers\":[{\"user\":\"mapred\",\"count\":3},{\"user\":\"spark\",\"count\":1}],\"totalCount\":4},{\"opType\":\"*\",\"topUsers\":[{\"user\":\"spark\",\"count\":18},{\"user\":\"hdfs\",\"count\":5},{\"user\":\"mapred\",\"count\":3},{\"user\":\"impala\",\"count\":1}],\"totalCount\":27},{\"opType\":\"delete\",\"topUsers\":[{\"user\":\"hdfs\",\"count\":1},{\"user\":\"spark\",\"count\":1}],\"totalCount\":2},{\"opType\":\"listCacheDirectives\",\"topUsers\":[{\"user\":\"hdfs\",\"count\":1}],\"totalCount\":1},{\"opType\":\"getfileinfo\",\"topUsers\":[{\"user\":\"spark\",\"count\":4},{\"user\":\"hdfs\",\"count\":1}],\"totalCount\":5},{\"opType\":\"create\",\"topUsers\":[{\"user\":\"hdfs\",\"count\":1},{\"user\":\"spark\",\"count\":1}],\"totalCount\":2},{\"opType\":\"open\",\"topUsers\":[{\"user\":\"spark\",\"count\":11},{\"user\":\"hdfs\",\"count\":1}],\"totalCount\":12}],\"windowLenMs\":60000},{\"ops\":[{\"opType\":\"listCachePools\",\"topUsers\":[{\"user\":\"hdfs\",\"count\":5},{\"user\":\"impala\",\"count\":3}],\"totalCount\":8},{\"opType\":\"listStatus\",\"topUsers\":[{\"user\":\"hue\",\"count\":13},{\"user\":\"mapred\",\"count\":12},{\"user\":\"spark\",\"count\":4}],\"totalCount\":29},{\"opType\":\"*\",\"topUsers\":[{\"user\":\"hue\",\"count\":56},{\"user\":\"spark\",\"count\":44},{\"user\":\"hdfs\",\"count\":24},{\"user\":\"mapred\",\"count\":12},{\"user\":\"impala\",\"count\":3}],\"totalCount\":139},{\"opType\":\"delete\",\"topUsers\":[{\"user\":\"hdfs\",\"count\":5},{\"user\":\"spark\",\"count\":4}],\"totalCount\":9},{\"opType\":\"listCacheDirectives\",\"topUsers\":[{\"user\":\"hdfs\",\"count\":5}],\"totalCount\":5},{\"opType\":\"getfileinfo\",\"topUsers\":[{\"user\":\"spark\",\"count\":8},{\"user\":\"hue\",\"count\":8},{\"user\":\"hdfs\",\"count\":5},{\"user\":\"mapred\",\"count\":1}],\"totalCount\":22},{\"opType\":\"rename\",\"topUsers\":[{\"user\":\"hue\",\"count\":2}],\"totalCount\":2},{\"opType\":\"mkdirs\",\"topUsers\":[{\"user\":\"hue\",\"count\":6}],\"totalCount\":6},{\"opType\":\"create\",\"topUsers\":[{\"user\":\"hdfs\",\"count\":5},{\"user\":\"spark\",\"count\":4}],\"totalCount\":9},{\"opType\":\"setPermission\",\"topUsers\":[{\"user\":\"hue\",\"count\":6}],\"totalCount\":6},{\"opType\":\"open\",\"topUsers\":[{\"user\":\"spark\",\"count\":32},{\"user\":\"hdfs\",\"count\":5}],\"totalCount\":37}],\"windowLenMs\":300000},{\"ops\":[{\"opType\":\"getEZForPath\",\"topUsers\":[{\"user\":\"hue\",\"count\":3}],\"totalCount\":3},{\"opType\":\"listCachePools\",\"topUsers\":[{\"user\":\"impala\",\"count\":17},{\"user\":\"hdfs\",\"count\":17}],\"totalCount\":34},{\"opType\":\"listStatus\",\"topUsers\":[{\"user\":\"mapred\",\"count\":64},{\"user\":\"hue\",\"count\":47},{\"user\":\"spark\",\"count\":13},{\"user\":\"hive\",\"count\":3}],\"totalCount\":127},{\"opType\":\"*\",\"topUsers\":[{\"user\":\"spark\",\"count\":226},{\"user\":\"hue\",\"count\":175},{\"user\":\"mapred\",\"count\":66},{\"user\":\"hdfs\",\"count\":53},{\"user\":\"impala\",\"count\":17},{\"user\":\"hive\",\"count\":3}],\"totalCount\":540},{\"opType\":\"delete\",\"topUsers\":[{\"user\":\"spark\",\"count\":13},{\"user\":\"hdfs\",\"count\":11}],\"totalCount\":24},{\"opType\":\"listCacheDirectives\",\"topUsers\":[{\"user\":\"hdfs\",\"count\":17}],\"totalCount\":17},{\"opType\":\"getfileinfo\",\"topUsers\":[{\"user\":\"hue\",\"count\":161},{\"user\":\"spark\",\"count\":46},{\"user\":\"hdfs\",\"count\":8},{\"user\":\"mapred\",\"count\":4}],\"totalCount\":219},{\"opType\":\"rename\",\"topUsers\":[{\"user\":\"hue\",\"count\":6}],\"totalCount\":6},{\"opType\":\"mkdirs\",\"topUsers\":[{\"user\":\"hue\",\"count\":15}],\"totalCount\":15},{\"opType\":\"create\",\"topUsers\":[{\"user\":\"spark\",\"count\":13},{\"user\":\"hdfs\",\"count\":11}],\"totalCount\":24},{\"opType\":\"setPermission\",\"topUsers\":[{\"user\":\"hue\",\"count\":24}],\"totalCount\":24},{\"opType\":\"open\",\"topUsers\":[{\"user\":\"spark\",\"count\":142},{\"user\":\"hdfs\",\"count\":11}],\"totalCount\":153}],\"windowLenMs\":1500000}]}",
"NumInMaintenanceLiveDataNodes":0,
"NumInMaintenanceDeadDataNodes":0,
"NumEnteringMaintenanceDataNodes":0
},




datanode
0. Hadoop:service=DataNode,name=DataNodeActivity-$host-$port
数据示例：
 {
    "name" : "Hadoop:service=DataNode,name=DataNodeActivity-ubuntu2-50010",
    "modelerType" : "DataNodeActivity-ubuntu2-50010",
    "tag.SessionId" : null,
    "tag.Context" : "dfs",
    "tag.Hostname" : "ubuntu2",
    "BytesWritten" : 37953802,
    "TotalWriteTime" : 8392,
    "BytesRead" : 190613906,
    "TotalReadTime" : 521649,
    "BlocksWritten" : 2520,
    "BlocksRead" : 4951,
    "BlocksReplicated" : 0,
    "BlocksRemoved" : 986,
    "BlocksVerified" : 0,
    "BlockVerificationFailures" : 0,
    "BlocksCached" : 0,
    "BlocksUncached" : 0,
    "ReadsFromLocalClient" : 4915,
    "ReadsFromRemoteClient" : 36,
    "WritesFromLocalClient" : 75,
    "WritesFromRemoteClient" : 2445,
    "BlocksGetLocalPathInfo" : 0,
    "RemoteBytesRead" : 96921,
    "RemoteBytesWritten" : 3672081,
    "RamDiskBlocksWrite" : 0,
    "RamDiskBlocksWriteFallback" : 0,
    "RamDiskBytesWrite" : 0,
    "RamDiskBlocksReadHits" : 0,
    "RamDiskBlocksEvicted" : 0,
    "RamDiskBlocksEvictedWithoutRead" : 0,
    "RamDiskBlocksEvictionWindowMsNumOps" : 0,
    "RamDiskBlocksEvictionWindowMsAvgTime" : 0.0,
    "RamDiskBlocksLazyPersisted" : 0,
    "RamDiskBlocksDeletedBeforeLazyPersisted" : 0,
    "RamDiskBytesLazyPersisted" : 0,
    "RamDiskBlocksLazyPersistWindowMsNumOps" : 0,
    "RamDiskBlocksLazyPersistWindowMsAvgTime" : 0.0,
    "FsyncCount" : 27,
    "VolumeFailures" : 0,
    "DatanodeNetworkErrors" : 977,
    "ReadBlockOpNumOps" : 4951,
    "ReadBlockOpAvgTime" : 585.4027598102631,
    "WriteBlockOpNumOps" : 2520,
    "WriteBlockOpAvgTime" : 12493.071876507476,
    "BlockChecksumOpNumOps" : 0,
    "BlockChecksumOpAvgTime" : 0.0,
    "CopyBlockOpNumOps" : 0,
    "CopyBlockOpAvgTime" : 0.0,
    "ReplaceBlockOpNumOps" : 0,
    "ReplaceBlockOpAvgTime" : 0.0,
    "HeartbeatsNumOps" : 9645,
    "HeartbeatsAvgTime" : 47.0,
    "BlockReportsNumOps" : 2,
    "BlockReportsAvgTime" : 15482.0,
    "IncrementalBlockReportsNumOps" : 2567,
    "IncrementalBlockReportsAvgTime" : 12.681344696969697,
    "CacheReportsNumOps" : 0,
    "CacheReportsAvgTime" : 0.0,
    "PacketAckRoundTripTimeNanosNumOps" : 0,
    "PacketAckRoundTripTimeNanosAvgTime" : 0.0,
    "FlushNanosNumOps" : 10265,
    "FlushNanosAvgTime" : 496772.8638928848,
    "FsyncNanosNumOps" : 54,
    "FsyncNanosAvgTime" : 5637848.388888889,
    "SendDataPacketBlockedOnNetworkNanosNumOps" : 11699,
    "SendDataPacketBlockedOnNetworkNanosAvgTime" : 3.0811991686990395E7,
    "SendDataPacketTransferNanosNumOps" : 11699,
    "SendDataPacketTransferNanosAvgTime" : 8547079.172947997
  }

1. JVm Metric


'''