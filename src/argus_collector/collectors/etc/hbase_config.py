# coding=utf8
"""
这个文件是用于配置HBase监控的文件

"""

region_file = '/etc/hbase/conf/regionservers'

config_path = '/etc/hbase/conf/hbase-site.xml'

host = 'localhost'

manual_charater = "region_server" ## 可选为region_server master 或者both，当为None时，采集器自动读取配置文件判断

master_port = 60010

master_metric = {
    'Hadoop:service=HBase,name=Master,sub=Server': [

        # 'tag.liveRegionServers',  #string
        # 'tag.deadRegionServers',  #string
        'averageLoad',  #int
        'numRegionServers',  #int
        'numDeadRegionServers',  #int

    ]
}


region_port = 60030

region_server_metric = {
    'Hadoop:service=HBase,name=RegionServer,sub=Server': [
        'totalRequestCount',   #int
        'blockCacheFreeSize',  #int
        'readRequestCount',    #总读次数 int
        'writeRequestCount',   #总写次数 int
        'flushedCellsCount',   # int
        'flushedCellsSize',    #flush到磁盘大小 int
        'flushQueueLength',    #  int
        'blockedRequestCount', #因memstore大于阈值而引发flush的次数 int
        'slowGetCount',        #请求完成时间超过1000ms的次数 int
        'storeCount',          #该Region Server管理的store个数 int
        'mutationsWithoutWALCount',  #int
        'mutationsWithoutWALSize',  #int
        'blockCacheHitCount',   #int
        'blockCacheMissCount',   # int
    ],
    'Hadoop:service=HBase,name=RegionServer,sub=IPC': [
        'numActiveHandler',    #int
    ],
    'Hadoop:service=HBase,name=RegionServer,sub=WAL': [
        'slowAppendCount',  #int
        'SyncTime_num_ops',   #int
        'SyncTime_max',       #float
        'SyncTime_mean',      #float
        'AppendTime_num_ops',    #int
        'AppendTime_max',   #float
        'AppendTime_mean',  #float
    ],
}