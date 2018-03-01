# coding=utf8

"""
这个文件是用于配置HDFS采集器的配置文件

"""


Namenode_jmx_port = 50070

manual_charater = "DataNode"  ## 可以选择为DataNode、NameNode、None(使用程序自动读取角色)

hdfs_config_path = '/etc/hadoop/conf/hdfs-site.xml'

NameNode_metric_dict = {

    'Hadoop:service=NameNode,name=FSNamesystem': [
        'CorruptBlocks',      #int
        'CapacityRemainingGB',    #int
        'Snapshots',   #int
        'MissingBlocks',   #int
    ],
    'Hadoop:service=NameNode,name=FSNamesystemState': [
        'VolumeFailuresTotal', #int
        'NumLiveDataNodes', #int
        'NumDeadDataNodes', #int
        'NumStaleDataNodes', #int
        'NumStaleStorages',  #int
    ]
}


DataNode_jmx_port = 50075

DataNode_metric_dict = {
    'Hadoop:service=DataNode,name=DataNodeActivity-$hostname-50010': [
        'BlockVerificationFailures', #int
        'BlockReportsAvgTime',  #float
        'BlockReportsNumOps',  #int
        'HeartbeatsAvgTime',   #float
        'HeartbeatsNumOps',    #int
        'DatanodeNetworkErrors', #int
        'VolumeFailures',  #int
        'ReplaceBlockOpNumOps',  #int
        'ReplaceBlockOpAvgTime',  #float

    ],

}

# host = 'localhost'
host = '192.168.0.180' ##被采集机器的ip（本机的ip）

