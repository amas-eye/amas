# Amas

[![Docker Automated build](https://img.shields.io/docker/automated/jrottenberg/ffmpeg.svg)](https://hub.docker.com/u/eacon/)

Language: [English](README.md) | [中文](README_ch.md)


## What is Amas
Amas is a monitor alert system based on big-data platform, with features below：
1. Provide metrics in full dimension, covering from operating-system, middleware, big-data platform(Hadoop/Spark/HBase/Kakfa...) to code level.
2. Highly extensible collector agent, support custom metrics written by different scripting language(Python/Perl/Shell/...).
3. Ability to read/write mass data quickly due to HBase/OpenTSDB on real production environment.
4. Web UI is sexy and powerful, yet easy to use.
5. Distributed asynchronous alert engine based on Python multiprocess and async/await, which makes it easily extend system processing ability.
6. Multi-channel and customizable notify method(wechat/mail/slack/api...).
7. Alerts could be aggregated by groups, preventing from "Alert Storm".
8. Distributed tracing collect and display based on Jagger, events are traceable.
9. Anomaly detection service based on machine learning, landing AIOps.
10. Due to micro-service architect, compatibly deploy with docker and docker-compose.
11. ...



## Technology Stack
* Program language：
    - (Backend)Python
    - (Web)Javascript
* Web Service：
    - Vue, ECharts, Webpack
    - Express(NodeJS)
* Backend Service：
    - HBase, OpenTSDB, MongoDB, Redis
    - Spark, Kafka
    - Jagger, Tornado
    - Pandas, Scikit-learn
    - Docker, Swarm


## Runtime Environment
* Linux(Kernel2.6+)
* Centos7(Recommend)


## Docker
So far, Amas repository is automated build on docker hub, you are recommended to run amas quickly by docker:
1. Install Docker
2. Create shell script below and execute:
```bash
#!/usr/bin/env bash

# create network for amas
docker network create amas

# run databases
# opentsdb(v2.3.0+)
# mongo(v3.10.0+)
# redis(v3.10.0+)
docker run -d -p 4242:4242 --name opentsdb --network amas eacon/docker-opentsdb
docker run -d -p 27017:27017 --name mongo --network amas mongo
docker run -d -p 6379:6379 --name redis --network amas redis

# run collector agent（Agent Manager included）：
docker run -d --name collector --network amas -p 8001:8001 eacon/argus_collector

# run alert process
docker run -d --name alert --network amas eacon/argus_alert

# run statistics process
docker run -d --name statistics --network amas eacon/argus_statistics

# run web server
docker run -d --name web --network amas -p 8080:8080 eacon/argus-web
```
3. Visit: open browser(try not to use ```localhost```, but ```127.0.0.1```):[http://127.0.0.1:8080](http://127.0.0.1:8080)
4. Init: execute web container to generate default account(username/password: admin/123):
```
docker exec -it web init_user
```


### Docker-Compose
With docker-compose installed，you could run amas as below：
1. git clone：
```
git clone https://github.com/amas-eye/amas.git; cd amas/docker/compose/
```
- Or just get that compose file：
```
mkdir amas; cd amas; curl https://raw.githubusercontent.com/amas-eye/amas/master/docker/compose/docker-compose.yml > docker-compose.yml
```
2. Execute command to run all containers up：
```
docker-compose up -d
```



## Metrics（Partly）
```
## metric 命名规范
- (总控件).控件.采集指标名   ts   value  host=<>  (node=master/slave[num])
  eg:
  hadoop.hbase.averageload ts  value host=$hostname  node=master1


## 系统基础服务性能指标
- net_dev.py
  cluster.net.dev.receive    网卡总接收字节数
  cluster.net.dev.transmit   网卡总发出字节数

- netstat.py（一般不使用配置给用户，暂时不标注）
  net.sockstat.num_sockets
  net.sockstat.num_timewait
  net.sockstat.sockets_inuse
  net.sockstat.num_orphans
  net.sockstat.memory
  net.sockstat.ipfragqueues
  net.stat.tcp.invalid_sack
  net.stat.tcp.delayedack
  net.stat.tcp.reording
  net.stat.tcp.abort
  net.stat.tcp.failed_accept
  net.stat.tcp.abort
  net.stat.tcp.syncookies
  net.stat.tcp.packetloss.recovery
  net.stat.tcp.congestion.recovery
  net.stat.tcp.invalid_sack
  net.stat.tcp.delayedack
  net.stat.tcp.retransmit
  net.stat.tcp.memory.pressure
  net.stat.tcp.congestion.recovery
  net.stat.tcp.memory.prune
  net.stat.tcp.invalid_sack
  net.stat.tcp.reording
  net.stat.tcp.delayedack
  net.stat.tcp.congestion.recovery
  net.stat.tcp.reording 1510732766 85 detectedby=fack
  net.stat.tcp.memory.prune
  net.stat.tcp.syncookies
  net.stat.tcp.receive.queue.full
  net.stat.tcp.failed_accept
  net.stat.tcp.congestion.recovery
  net.stat.tcp.retransmit
  net.stat.tcp.reording
  net.stat.tcp.abort.failed
  net.stat.tcp.packetloss.recovery
  net.stat.udp.datagrams
  net.stat.udp.errors


- ifstat.py
  proc.net.bytes    网卡的字节数 （需要看方向，方向在tag中会显示）
  proc.net.packets  网卡的包的数量（方向是in/out)
  proc.net.errs     网卡错误包的数
  proc.net.dropped  网卡丢包书
  proc.net.fifo.errs 网卡队列错误数
  proc.net.frame.errs 网卡帧的错误数
  proc.net.compressed 网卡是否启用压缩



- mysql.py
    mysql.innodb.buffer_pool_free                      InnoDB 缓冲池空闲页面数  #show status; Innodb_buffer_pool_pages_free
    mysql.innodb.buffer_pool_total		               InnoDB 缓冲池的总页数    #show status; Innodb_buffer_pool_pages_total
    mysql.innodb.buffer_pool_used		               InnoDB 缓冲池中已使用的页数 #show status; Innodb_buffer_pool_pages_free
    mysql.innodb.buffer_pool_utilization	fractions  InnoDB 的缓冲池的利用率  #show status;total-free/toatl
    mysql.innodb.current_row_locks	                   The number of current row locks.    #show status;Innodb_row_lock_current_waits
    mysql.innodb.data_reads	     	                   数据的读取速率 (读的次数/s)  #show status; Innodb_data_reads
    mysql.innodb.data_writes		                   数据的写速率 (写的次数/s) #show status; Innodb_data_writes
    mysql.innodb.mutex_os_waits	events/second	       The rate of mutex OS waits.
    mysql.innodb.mutex_spin_rounds	events/second	   The rate of mutex spin rounds.
    mysql.innodb.mutex_spin_waits	events/second	   The rate of mutex spin waits.
    mysql.innodb.os_log_fsyncs		                   fsync 写入日志文件的速率（写的次数/s）  #show status; Innodb_os_log_fsyncs
    mysql.innodb.row_lock_time		                   花费在 acquring 行锁上的时间（millisecond/s）#show status; Innodb_row_lock_time
    mysql.innodb.row_lock_waits		                   行锁每秒要等待的次数（event/s） #show status; Innodb_row_lock_waits
    mysql.net.connections	connections/second	       连接到服务器的速率（连接数量/s） #
    mysql.net.max_connections		                   服务器启动同时使用的最大数目连接数   # show status;Max_used_connections
    mysql.performance.com_delete	                   删除语句的速率（次数/s） #  #show status;Com_delete
    mysql.performance.com_delete_multi	               删除多语句的速率（次数/s）#show status;Com_delete_multi
    mysql.performance.com_insert		               插入语句的速率（次数/s）  #show status;Com_insert
    mysql.performance.com_insert_select	               插入 SELECT 语句的速率（次数/s）#show status;Com_insert_select
    mysql.performance.com_replace_select               代替 SELECT 语句的速度（次数/s） #show status;Com_replace_select
    mysql.performance.com_select		               SELECT 语句的速度（次数/s） # show status;Com_select
    mysql.performance.com_update		               更新语句的速度（次数/s）     # show status;Com_update
    mysql.performance.com_update_multi	               更新多语句的速度（次数/s） #show status;Com_update_multi
    mysql.performance.created_tmp_disk_tables	       执行语句时每秒创建的服务器内部磁盘上的临时表的数量 （表数量/s） #show status;Created_tmp_disk_tables
    mysql.performance.created_tmp_files		           每秒创建临时文件的数量 (文件数/s)   #show stats;Created_tmp_files
    mysql.performance.created_tmp_tables	           每秒执行语句时创建的服务器内部临时表的数量（表数量/s）#show stats;Created_tmp_tables
    mysql.performance.kernel_time	     	           MySQL 在内核空间中花费的 CPU 时间占比
    mysql.performance.key_cache_utilization	fractions  键缓存利用率 (百分比)
    mysql.performance.open_files	 	               打开的文件数  #show status; Open_files
    mysql.performance.open_tables	 	               打开的表数量  #show status; Open_tables
    mysql.performance.qcache_hits	 	               查询缓存命中率  #show status; Qcache_hits
    mysql.performance.queries	    	               查询的速率 (次数/s)  #show status; Queries
    mysql.performance.questions	 	                   服务器执行的语句的速率（次数/s）#show status; Questions
    mysql.performance.slow_queries	  	               慢查询的速率（次数/s）   #show status; Slow_queries
    mysql.performance.table_locks_waited		       由于表锁定请求无法处理需要等待的总次数 #show status; Table_locks_waited
    mysql.performance.threads_connected	 	           当前打开的连接的数量   #show status;Threads_connected
    mysql.performance.threads_running	 	           正在运行的线程数       #show status;Threads_running
    mysql.performance.user_time	percent	               MySQL 在用户空间中花费的 CPU 时间占比
    mysql.replication.seconds_behind_master	seconds	   主服务器（master）和从服务器（slave）之间的滞后时间  #show slave status;Seconds_Behind_Master
    mysql.replication.slave_running		               一个布尔值，判断该服务器是否为连接到主服务器（master）的从服务器（slave） #show slave status 对两个thread进行判断
    mysql.performance.lock_table                       #show status; Com_lock_tables


## 大数据平台性能指标

对于大数据中有进行jvm采集的部分指标说明(hdfs、hbase、mapreduce)
- hadoop.xx.jvm.$metric
具体metric如下
MemNonHeapUsedM
MemNonHeapCommittedM
MemNonHeapMaxM
MemHeapUsedM
MemHeapCommittedM
MemHeapMaxM
MemMaxM
GcCountParNew
GcTimeMillisParNew
GcCountConcurrentMarkSweep
GcTimeMillisConcurrentMarkSweep
GcCount                 ## Gc的总次数
GcTimeMillis            ## Gc的总时间（单位：毫秒）
ThreadsNew              ## 新建线程
ThreadsRunnable         ## 运行线程
ThreadsBlocked          ## 阻塞线程
ThreadsWaiting          ## 等待线程是
ThreadsTimedWaiting     ## 限时等待线程数（有timeout）
ThreadsTerminated       ## 终结线程
LogFatal                ## 严重错误
LogError                ## 错误
LogWarn
LogInfo


- hbase.py
  #(通过获取配置文件得到本机运行的项目)
  node = master[num]
  - hadoop.hbase.Master.mergePlanCount             ###
  - hadoop.hbase.Master.splitPlanCount             ###
  - hadoop.hbase.Master.averageLoad                ###平均负载
  - hadoop.hbase.Master.numRegionServers           ###存活的Region
  - hadoop.hbase.Master.numDeadRegionServers       ###死去的Region
  - hadoop.hbase.Master.clusterRequests            ###集群总请求数
  - hadoop.hbase.Master.ritOldestAge                           # Master管理下的region 状态迁移的最长时间
  - hadoop.hbase.Master.ritCountOverThreshold                  # 状态迁移超过阈值（默认为60秒）
  - hadoop.hbase.Master.BulkAssign_num_ops                     # 批量迁移状态的操作数
  - hadoop.hbase.Master.BulkAssign_min                         # 批量迁移状态的最小用时
  - hadoop.hbase.Master.BulkAssign_max                         # 批量迁移状态的最长用时
  - hadoop.hbase.Master.BulkAssign_mean                        # 批量迁移状态的平均用时
  - hadoop.hbase.Master.ritCount                            # 转移状态中的regionserver
  - hadoop.hbase.Master.Assign_num_ops                      # 单个迁移状态的操作数
  - hadoop.hbase.Master.Assign_min                          # 单个迁移状态的最短时间
  - hadoop.hbase.Master.Assign_max                          # 单个迁移状态的最长时间
  - hadoop.hbase.Master.Assign_mean                         # 单个迁移状态的平均时间
  - hadoop.hbase.Master.queueSize                           # 排队队列大小
  - hadoop.hbase.Master.numCallsInGeneralQueue              # 普通队列调用数
  - hadoop.hbase.Master.numCallsInReplicationQueue          # 副本队列调用数
  - hadoop.hbase.Master.numCallsInPriorityQueue             # 优先队列调用数
  - hadoop.hbase.Master.numOpenConnections                  # 保持的链接数的大小
  - hadoop.hbase.Master.numActiveHandler                    # 活跃的handler
  - hadoop.hbase.Master.numGeneralCallsDropped              # 丢失的普通请求数
  - hadoop.hbase.Master.numLifoModeSwitches                 # 栈模式切换数
  - hadoop.hbase.Master.receivedBytes                       # 接收到的数量
  - hadoop.hbase.Master.exceptions.RegionMovedException     # Region状态迁移错误数
  - hadoop.hbase.Master.exceptions.multiResponseTooLarge    # 接收到多个相应超出限定阈值
  - hadoop.hbase.Master.authenticationSuccesses             # 认证成功数
  - hadoop.hbase.Master.authorizationFailures               # 授权失败数
  - hadoop.hbase.Master.exceptions.RegionTooBusyException   # Region_server任务过多导致错误的数量
  - hadoop.hbase.Master.exceptions.FailedSanityCheckException #
  - hadoop.hbase.Master.exceptions.UnknownScannerException    # 未知扫描错误
  - hadoop.hbase.Master.exceptions.OutOfOrderScannerNextException # 乱序扫描错误
  - hadoop.hbase.Master.exceptions                          # 总错误数
  - hadoop.hbase.Master.ProcessCallTime_num_ops             # 总操作数
  - hadoop.hbase.Master.ProcessCallTime_min                 # 处理时间最小值
  - hadoop.hbase.Master.ProcessCallTime_max                 # 处理时间最大值
  - hadoop.hbase.Master.ProcessCallTime_mean                # 处理时间平均值
  - hadoop.hbase.Master.authenticationFallbacks              # 认证退却
  - hadoop.hbase.Master.exceptions.NotServingRegionException #
  - hadoop.hbase.Master.exceptions.callQueueTooBig           # 等待队列满错误
  - hadoop.hbase.Master.authorizationSuccesses               # 授权成功
  - hadoop.hbase.Master.exceptions.ScannerResetException     # 扫描器重置错误
  - hadoop.hbase.Master.sentBytes                            # 发送字节数
  - hadoop.hbase.Master.QueueCallTime_num_ops                # 队列调用次数
  - hadoop.hbase.Master.QueueCallTime_min                    # 调用最短时间
  - hadoop.hbase.Master.QueueCallTime_max                    # 调用最长时间
  - hadoop.hbase.Master.QueueCallTime_mean                   # 调用平均时间
  - hadoop.hbase.Master.authenticationFailures               # 认证失败次数

  node = RegionServer
  - hadoop.hbase.RegionServer.jvm.ThreadsWaiting
  - hadoop.hbase.RegionServer.jvm.ThreadsTerminated
  - hadoop.hbase.RegionServer.jvm.LogError
  - hadoop.hbase.RegionServer.jvm.MemNonHeapCommittedM
  - hadoop.hbase.RegionServer.jvm.GcTimeMillis
  - hadoop.hbase.RegionServer.jvm.MemHeapMaxM
  - hadoop.hbase.RegionServer.jvm.MemHeapUsedM
  - hadoop.hbase.RegionServer.jvm.ThreadsBlocked
  - hadoop.hbase.RegionServer.jvm.LogWarn
  - hadoop.hbase.RegionServer.jvm.GcTimeMillisConcurrentMarkSweep
  - hadoop.hbase.RegionServer.jvm.GcTimeMillisParNew
  - hadoop.hbase.RegionServer.jvm.MemHeapCommittedM
  - hadoop.hbase.RegionServer.jvm.GcCountParNew
  - hadoop.hbase.RegionServer.jvm.MemNonHeapMaxM
  - hadoop.hbase.RegionServer.jvm.GcCountConcurrentMarkSweep
  - hadoop.hbase.RegionServer.jvm.ThreadsNew
  - hadoop.hbase.RegionServer.jvm.ThreadsRunnable
  - hadoop.hbase.RegionServer.jvm.GcCount
  - hadoop.hbase.RegionServer.jvm.ThreadsTimedWaiting
  - hadoop.hbase.RegionServer.jvm.MemMaxM
  - hadoop.hbase.RegionServer.jvm.LogInfo
  - hadoop.hbase.RegionServer.jvm.LogFatal
  - hadoop.hbase.RegionServer.jvm.MemNonHeapUsedM
  ## 上面为 JVm通用部分，请查看JVM部分解释，此处不再重复

  - hadoop.hbase.RegionServer.RSServer.Replay_max                      # 最长重发=放时间
  - hadoop.hbase.RegionServer.RSServer.regionCount                     # RegionServer所拥有的Region数量
  - hadoop.hbase.RegionServer.RSServer.storeFileCount                  # 被RegionServer管理的文件个数
  - hadoop.hbase.RegionServer.RSServer.Mutate_num_ops                  # 修改操作数
  - hadoop.hbase.RegionServer.RSServer.totalRequestCount               # 总请求数
  - hadoop.hbase.RegionServer.RSServer.Increment_max                   # 最长新增时间
  - hadoop.hbase.RegionServer.RSServer.writeRequestCount               # 写请求数
  - hadoop.hbase.RegionServer.RSServer.Increment_mean                  # 最短新增时间
  - hadoop.hbase.RegionServer.RSServer.percentFilesLocal               # 本Regionserver中本地可以应对请求的百分比
  - hadoop.hbase.RegionServer.RSServer.Append_num_ops                  # 追加操作数
  - hadoop.hbase.RegionServer.RSServer.mutationsWithoutWALCount        # 写入时带上标记来绕过aheadlog的次数
  - hadoop.hbase.RegionServer.RSServer.storeFileSize                   # 存储文件的总大小
  - hadoop.hbase.RegionServer.RSServer.Get_mean                        # 平均获取时间
  - hadoop.hbase.RegionServer.RSServer.Increment_min                   # 最短新增时间
  - hadoop.hbase.RegionServer.RSServer.Replay_num_ops                  # 重放操作数
  - hadoop.hbase.RegionServer.RSServer.blockCacheExpressHitPercent     # 请求可以请求到缓存的数量占总请求数的时间
  - hadoop.hbase.RegionServer.RSServer.Get_num_ops                     # 获取操作数
  - hadoop.hbase.RegionServer.RSServer.Get_max                         # 最长获取时间
  - hadoop.hbase.RegionServer.RSServer.readRequestCount                # 读取请求的数量
  - hadoop.hbase.RegionServer.RSServer.blockCacheHitCount              # 请求到缓存的块数量
  - hadoop.hbase.RegionServer.RSServer.slowGetCount                    # 读取的慢操作次数
  - hadoop.hbase.RegionServer.RSServer.Append_max                      # 追加最长操作时间
  - hadoop.hbase.RegionServer.RSServer.Increment_num_ops               # 新增数据操作
  - hadoop.hbase.RegionServer.RSServer.Mutate_min                      # 最短修改数据时间
  - hadoop.hbase.RegionServer.RSServer.updatesBlockedTime              # 更新阻塞时间
  - hadoop.hbase.RegionServer.RSServer.blockCacheMissCount             # 没有请求到缓存的块的数量
  - hadoop.hbase.RegionServer.RSServer.Append_mean                     # 平均追加时间
  - hadoop.hbase.RegionServer.RSServer.hlogFileCount                   # 比日志超前的写入数量
  - hadoop.hbase.RegionServer.RSServer.Replay_min                      # 重放最短时间
  - hadoop.hbase.RegionServer.RSServer.Mutate_max                      # 修改最长时间
  - hadoop.hbase.RegionServer.RSServer.Mutate_mean                     # 平均修改时间
  - hadoop.hbase.RegionServer.RSServer.Get_min                         # 最短获取时间
  - hadoop.hbase.RegionServer.RSServer.Append_min                      # 最短追加时间
  - hadoop.hbase.RegionServer.RSIpc.exceptions.UnknownScannerException # 未知扫描器错误
  - hadoop.hbase.RegionServer.RSIpc.ProcessCallTime_mean               # 最短处理时间
  - hadoop.hbase.RegionServer.RSIpc.numCallsInPriorityQueue            # 优先队列调用次数
  - hadoop.hbase.RegionServer.RSIpc.QueueCallTime_min                  # 队列最短调用时间
  - hadoop.hbase.RegionServer.RSIpc.ProcessCallTime_num_ops            # 处理的次数
  - hadoop.hbase.RegionServer.RSIpc.QueueCallTime_mean                 # 队列调用平均时间
  - hadoop.hbase.RegionServer.RSIpc.exceptions.multiResponseTooLarge   # 响应大小超过阈值错误
  - hadoop.hbase.RegionServer.RSIpc.QueueCallTime_num_ops              # 队列调用次数
  - hadoop.hbase.RegionServer.RSIpc.ProcessCallTime_max                # 最长处理时间
  - hadoop.hbase.RegionServer.RSIpc.numCallsInGeneralQueue             # 普通队列调用次数
  - hadoop.hbase.RegionServer.RSIpc.numCallsInReplicationQueue         # 副本队列调用次数
  - hadoop.hbase.RegionServer.RSIpc.numActiveHandler                   # 活跃的连接数
  - hadoop.hbase.RegionServer.RSIpc.QueueCallTime_max                  # 队列最长调用时间
  - hadoop.hbase.RegionServer.RSIpc.ProcessCallTime_min                # 最短处理时间
  - hadoop.hbase.RegionServer.RSIpc.exceptions.RegionMovedException    # region移动错误



- hdfs.py
  #(通过获取配置文件得到本机运行的项目)
  node = namenode

  - hadoop.hdfs.NameNode.jvm.ThreadsWaiting
  - hadoop.hdfs.NameNode.jvm.MemNonHeapUsedM
  - hadoop.hdfs.NameNode.jvm.MemNonHeapCommittedM
  - hadoop.hdfs.NameNode.jvm.GcNumInfoThresholdExceeded
  - hadoop.hdfs.NameNode.jvm.GcTimeMillis
  - hadoop.hdfs.NameNode.jvm.MemHeapMaxM
  - hadoop.hdfs.NameNode.jvm.MemHeapUsedM
  - hadoop.hdfs.NameNode.jvm.ThreadsBlocked
  - hadoop.hdfs.NameNode.jvm.LogWarn
  - hadoop.hdfs.NameNode.jvm.LogError
  - hadoop.hdfs.NameNode.jvm.MemHeapCommittedM
  - hadoop.hdfs.NameNode.jvm.MemNonHeapMaxM
  - hadoop.hdfs.NameNode.jvm.ThreadsNew
  - hadoop.hdfs.NameNode.jvm.ThreadsRunnable
  - hadoop.hdfs.NameNode.jvm.GcCount
  - hadoop.hdfs.NameNode.jvm.ThreadsTimedWaiting
  - hadoop.hdfs.NameNode.jvm.MemMaxM
  - hadoop.hdfs.NameNode.jvm.GcTotalExtraSleepTime
  - hadoop.hdfs.NameNode.jvm.GcNumWarnThresholdExceeded
  - hadoop.hdfs.NameNode.jvm.LogInfo
  - hadoop.hdfs.NameNode.jvm.LogFatal
  - hadoop.hdfs.NameNode.jvm.ThreadsTerminated
  # 与通用的JVM指标相同，具体详情请看JVM部分解析


  - hadoop.hdfs.NameNode.Activity.RenameSnapshotOps                    #
  - hadoop.hdfs.NameNode.Activity.TotalFileOps                         #
  - hadoop.hdfs.NameNode.Activity.GetAdditionalDatanodeOps             #
  - hadoop.hdfs.NameNode.Activity.BlockReportNumOps                    #
  - hadoop.hdfs.NameNode.Activity.TransactionsNumOps                   # Total number of Journal transactions
  - hadoop.hdfs.NameNode.Activity.BlockReportAvgTime                   #
  - hadoop.hdfs.NameNode.Activity.CreateSymlinkOps                     #
  - hadoop.hdfs.NameNode.Activity.StorageBlockReportOps                #
  - hadoop.hdfs.NameNode.Activity.FilesRenamed                         #
  - hadoop.hdfs.NameNode.Activity.SafeModeTime                         # 运行在安全模式的时间
  - hadoop.hdfs.NameNode.Activity.FilesInGetListingOps                 #
  - hadoop.hdfs.NameNode.Activity.BlockOpsQueued                       # 排队的块操作相关次数
  - hadoop.hdfs.NameNode.Activity.GetLinkTargetOps                     #
  - hadoop.hdfs.NameNode.Activity.PutImageNumOps                       # Total number of fsimage uploads to SecondaryNameNode
  - hadoop.hdfs.NameNode.Activity.GetEditAvgTime                       #
  - hadoop.hdfs.NameNode.Activity.SnapshotDiffReportOps                #
  - hadoop.hdfs.NameNode.Activity.CacheReportNumOps                    #
  - hadoop.hdfs.NameNode.Activity.FsImageLoadTime                      #
  - hadoop.hdfs.NameNode.Activity.TransactionsAvgTime                  #
  - hadoop.hdfs.NameNode.Activity.GetListingOps                        #
  - hadoop.hdfs.NameNode.Activity.GetEditNumOps                        #
  - hadoop.hdfs.NameNode.Activity.AddBlockOps                          # Total number of addBlock operations succeeded
  - hadoop.hdfs.NameNode.Activity.AllowSnapshotOps                     # Total number of allowSnapshot operations
  - hadoop.hdfs.NameNode.Activity.BlockReceivedAndDeletedOps           #
  - hadoop.hdfs.NameNode.Activity.CacheReportAvgTime                   #
  - hadoop.hdfs.NameNode.Activity.TransactionsBatchedInSync            #
  - hadoop.hdfs.NameNode.Activity.ListSnapshottableDirOps              #
  - hadoop.hdfs.NameNode.Activity.FilesTruncated                       #
  - hadoop.hdfs.NameNode.Activity.DisallowSnapshotOps                  #
  - hadoop.hdfs.NameNode.Activity.GetBlockLocations                    #
  - hadoop.hdfs.NameNode.Activity.GetImageNumOps                       #
  - hadoop.hdfs.NameNode.Activity.SyncsAvgTime                         #
  - hadoop.hdfs.NameNode.Activity.CreateSnapshotOps                    # 创建快照的数量
  - hadoop.hdfs.NameNode.Activity.DeleteSnapshotOps                    # 删除快照的数量
  - hadoop.hdfs.NameNode.Activity.SyncsNumOps                          #
  - hadoop.hdfs.NameNode.Activity.FileInfoOps                          #
  - hadoop.hdfs.NameNode.Activity.CreateFileOps                        # 创建文件操作数
  - hadoop.hdfs.NameNode.Activity.GetImageAvgTime                      #
  - hadoop.hdfs.NameNode.Activity.BlockOpsBatched                      #
  - hadoop.hdfs.NameNode.Activity.FilesDeleted                         # 文件删除数
  - hadoop.hdfs.NameNode.Activity.PutImageAvgTime                      #
  - hadoop.hdfs.NameNode.Activity.DeleteFileOps                        # 删除文件操作数
  - hadoop.hdfs.NameNode.Activity.FilesCreated                         # 文件创建数
  - hadoop.hdfs.NameNode.Activity.FilesAppended                        # Total number of files and directories created by create or mkdir operations
  - hadoop.hdfs.NameNode.FSState.NumDecomDeadDataNodes                 # Total number of files appended
  - hadoop.hdfs.NameNode.FSState.BlockDeletionStartTime                #
  - hadoop.hdfs.NameNode.FSState.NumLiveDataNodes                      #
  - hadoop.hdfs.NameNode.FSState.FilesTotal                            # Current number of files and directories
  - hadoop.hdfs.NameNode.FSState.SnapshotStats                         #
  - hadoop.hdfs.NameNode.FSState.PendingReplicationBlocks              # Current number of blocks pending to be replicated
  - hadoop.hdfs.NameNode.FSState.NumEncryptionZones                    #
  - hadoop.hdfs.NameNode.FSState.PendingDeletionBlocks                 # Current number of blocks pending deletion
  - hadoop.hdfs.NameNode.FSState.UnderReplicatedBlocks                 #
  - hadoop.hdfs.NameNode.FSState.FsLockQueueLength                     #
  - hadoop.hdfs.NameNode.FSState.FSState                               #
  - hadoop.hdfs.NameNode.FSState.ScheduledReplicationBlocks            # Current number of blocks scheduled for replications
  - hadoop.hdfs.NameNode.FSState.TotalLoad                             # Current number of connections
  - hadoop.hdfs.NameNode.FSState.VolumeFailuresTotal                   #
  - hadoop.hdfs.NameNode.FSState.EstimatedCapacityLostTotal            #
  - hadoop.hdfs.NameNode.FSState.CapacityTotal                         #
  - hadoop.hdfs.NameNode.FSState.BlocksTotal                           # Current number of allocated blocks in the system
  - hadoop.hdfs.NameNode.FSState.NumStaleDataNodes                     #
  - hadoop.hdfs.NameNode.FSState.NumDeadDataNodes                      # 死去的DataNode数量
  - hadoop.hdfs.NameNode.FSState.NumStaleStorages                      # 过期的DataNode数量
  - hadoop.hdfs.NameNode.FSState.NumDecomLiveDataNodes                 #
  - hadoop.hdfs.NameNode.FSState.CapacityUsed                          # Current used capacity across all DataNodes in bytes
  - hadoop.hdfs.NameNode.FSState.NumDecommissioningDataNodes           #
  - hadoop.hdfs.NameNode.FSState.CapacityRemaining                     #
  - hadoop.hdfs.NameNode.FSState.MaxObjects                            #



  node = datanode
  - hadoop.hdfs.BlockVerificationFailures  检查失败的块的个数
  - hadoop.hdfs.BlockReportsAvgTime      被阻塞的平均时间
  - hadoop.hdfs.BlockReportsNumOps       被阻塞的操作总数
  - hadoop.hdfs.HeartbeatsAvgTime        平均心跳时间
  - hadoop.hdfs.DatanodeNetworkErrors    DadaNode节点网络错误
  - hadoop.hdfs.HeartbeatsNumOps         心跳个数
  - hadoop.hdfs.ReplaceBlockOpNumOps     替换操作发生的总数
  - hadoop.hdfs.VolumeFailures           发生错误的volume的个数
  - hadoop.hdfs.ReplaceBlockOpAvgTime    替换操作使用的平均时间
  - hadoop.hdfs.datanode.rpc.RpcSlowCalls       ##  慢调用次数
  - hadoop.hdfs.datanode.rpc.RpcQueueTimeAvgTime ## 平均排队时间（单位为毫秒）
  - hadoop.hdfs.datanode.rpc.RpcClientBackoff   ##
  - hadoop.hdfs.datanode.rpc.NumOpenConnections ## 保持的连接数
  - hadoop.hdfs.datanode.rpc.RpcQueueTimeNumOps ## 调用的总次数
  - hadoop.hdfs.datanode.rpc.RpcAuthorizationFailures
  - hadoop.hdfs.datanode.rpc.RpcAuthenticationSuccesses ##
  - hadoop.hdfs.datanode.rpc.RpcProcessingTimeAvgTime  ## 调用的平均处理时间
  - hadoop.hdfs.datanode.rpc.RpcProcessingTimeNumOps   ## 与调用的总次数相同
  - hadoop.hdfs.datanode.rpc.RpcAuthenticationFailures ## 远程调用的认证成功次数
  - hadoop.hdfs.datanode.rpc.RpcAuthorizationSuccesses ## 远程调用的认证失败次数
  - hadoop.hdfs.datanode.rpc.CallQueueLength   ## 远程调用队列的长度


- hive.py
    node = metastore
    要获取hive_server 和 hive_metastore的PID
    - hadoop.hive.metastore.linkconut   #metastore的连接数 ，使用lsof -i|grep "$Pid"
      # 通过pidstat来获取的参数
      -- pidstat -u
    - hadoop.hive.cpu_user_rate         用户态cpu使用率
    - hadoop.hive.cpu_system_rate       内核态cpu使用率
      -- pidstat -d
    - hadoop.hive.disk.read_speed      读取速度
    - hadoop.hive.disk.write_speed     写入速度
      -- pidstat -r
    - hadoop.hive.mem_virtual          虚拟内存大小
    - hadoop.hive.mem_rss

    - hadoop.hive.db_connected #0为失败，1为成功(考虑中),如何复用jdbc的连接


    node = hive_server
    # 通过pidstat来获取的参数
      -- pidstat -u
    - hadoop.hive.cpu_user_rate
    - hadoop.hive.cpu_system_rate
      -- pidstat -d
    - hadoop.hive.disk.read_speed
    - hadoop.hive.disk.write_speed
      -- pidstat -r
    - hadoop.hive.mem_virtual
    - hadoop.hive.mem_rss

    - hadoop.hive.metastore_total #读配置文件
    - hadoop.hive.metastore_alive #通过lsof -i | grep "^($pid='hiveserver'pid)"进行获取
    - hadoop.hive.metastore_dead  #dead = total-alive


kafka.py(采集方法是使用jolokia/list/mbean的大类
    node = Producer


    node = Consumer


    node = broker
        Mbean: kafka.server:type=KafkaServer,name=BrokerState
        - kafka.broker.brokerstate [value]    #broker状态
        Mbean: kafka.server:type=KafkaServer,name=ClusterId
        - kafka.broker.clusterid    [value]   #集群id
        Mbean: kafka.server:type=DelayedOperationPurgatory,name=NumDelayedOperations,delayedOperation=Fetch
        - kafka.broker.delayfetch   [value]   #broker延迟的被消费操作数
        Mbean: kafka.server:type=DelayedOperationPurgatory,name=NumDelayedOperations,delayedOperation=Produce
        - kafka.broker.delayproduce [value]   #broker延迟的生产操作数
        Mbean: kafka.server:type=DelayedOperationPurgatory,name=NumDelayedOperations,delayedOperation=Heartbeat
        - kafka.broker.delayheartbeat [value] #broker心跳书
        Mbean: kafka.server:type=DelayedOperationPurgatory,name=NumDelayedOperations,delayedOperation=Topic
        - kafka.broker.delaytopic   [value]   #broker的topic延迟数
        Mbean: kafka.server:type=DelayedOperationPurgatory,name=NumDelayedOperations,delayedOperation=Rebalance
        - kafka.broker.delayrebalance [value]   #broker再平衡数
        Mbean: kafka.server:type=ReplicaManager,name=PartitionCount
        - kafka.broker.partitioncount [value] #broker partition数
        Mbean: kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions
        - kafka.broker.underreplicatedpartitions [value] #broker受管理的partition数量
        Mbean: kafka.server:type=ReplicaManager,name=IsrExpandsPerSec
        - kafka.broker.isrexpandspeed [count]   #扩展速度
        Mbean: kafka.server:type=ReplicaManager,name=IsrShrinksPerSec
        - kafka.broker.isrshrinkspeed [count]   #收缩速度

        node = topic
        Mbean: kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec
        - kafka.broker.topic.byteinpersecond [count] # topic的写入字节数（每秒）
        Mbean: kafka.server:type=BrokerTopicMetrics,name=BytesOutPerSec
        - kafka.broker.topic.byteoutpersecond [count] # topic的读取字节数（每秒）
        Mbean: kafka.server:type=BrokerTopicMetrics,name=BytesRejectedPerSec
        - kafka.broker.topic.byterejectpersecond [count] #topic的拒绝数*每秒）
        Mbean: kafka.server:type=BrokerTopicMetrics,name=TotalFetchRequestsPerSec
        - kafka.broker.topic.totalfetchrequestpersecond [count] # topic发出的请求数
        Mbean: kafka.server:type=BrokerTopicMetrics,name=TotalProduceRequestsPerS ec
        - kafka.broker.topic.totalproducerequestpersecond [count] # topic产出的请求数

     node = controller
        Mbean: kafka.controller:type=KafkaController,name=OfflinePartitionsCount
        - kafka.controller.offlinepartitioncount [value]  #下线的分区数量
        Mbean: kafka.controller:type=KafkaController,name=ActiveControllerCount
        - kafka.controller.activecontrollerconut [value]  #活跃的controller数量
        Mbean: kafka.controller:type=ControllerStats,name=UncleanLeaderElectionsPerSec
        - kafka.controller.uncleanLeaderElection [count]  #未完成的选举树
        Mbean: kafka.controller:type=ControllerStats,name=LeaderElectionRateAndTimeMs
        - kafka.controller.leaderelectiontime #主选举时间


impala.py
    node = catalogd
        - impala.catalogd.tcmalloc.bytes-in-use   # catalogd程序使用的内存
        - impala.catalogd.tcmalloc.pageheap-free-bytes  # page堆中空闲的内存
        - impala.catalogd.tcmalloc.pageheap-unmapped-bytes # page堆中未映射的内存
        - impala.catalogd.tcmalloc_physical_bytes_reserved # 预留的物理内存
        - impala.catalogd.tcmalloc.total-bytes-reserved  #总预留内存
        - impala.catalogd.statestore-subscriber.heartbeat-interval-time.last  #上一次与statestore的心跳时间
        - impala.catalogd.statestore-subscriber.heartbeat-interval-time.min   #最短的心跳时间
        - impala.catalogd.statestore-subscriber.heartbeat-interval-time.max   #最长的心跳时间
        - impala.catalogd.statestore-subscriber.heartbeat-interval-time.avg   #平均的心跳时间
        - impala.catalogd.statestore-subscriber.last-recovery-duration        #上一次回复的耗时
        - impala.catalogd.statestore-subscriber.statestore.client-cache.clients-in-use #正在使用statestore的客户端数量
        - impala.catalogd.statestore_subscriber_statestore_client_cache_total_clients #statestore缓存的总客户端数量


    node = statestore
        - impala.statestore.statestore.live-backends  # 存活的statestore数量
        - impala.statestore.total-key-size-bytes      # 总共的键的所用内存字节数
        - impala.statestore.total-topic-size-bytes    # 总共的话题所用内存字节数
        - impala.statestore.total-value-size-bytes    # statestore中全部值和话题的总和
        - impala.statestore.subscriber-heartbeat.client-cache.clients-in-use # 正在使用的客户端（catalogd）个数
        - impala.statestore.subscriber-heartbeat.client-cache.total-clients  # 总客户端（catalogd）个数，
        - impala.statestore.tcmalloc.bytes-in-use     # statestore所使用的内存
        - impala.statestore.tcmalloc.pageheap-free-bytes # statestore中page堆空闲的内存
        - impala.statestore.tcmalloc.pageheap-unmapped-bytes # statestore中未映射的内存大小
        - impala.statestore.tcmalloc.physical-bytes-reserved # statestore预留的物理内存大小
        - impala.statestore.tcmalloc.total-bytes-reserved    #statestore的总预留内存大小
        - impala.statestore.thread-manager.running-threads   #运行的线程个数
        - impala.statestore.thread-manager.total-threads-created # 创建的线程总个数

    node = impalad
        - impala.impalad.hash-table.total-bytes   #目前被分配的Hash表大小
        - impala.impalad.io-mgr.cached-bytes-read #读取的缓存字节数
        - impala.impalad.io-mgr.bytes-written     #写入的字节数
        - impala.impalad.io-mgr.bytes-read        #io阅读的字节数
        - impala.impalad.io-mgr.local-bytes-read  #本地io阅读的字节数
        - impala.impalad.io-mgr.total-bytes       #  io的总字节数
        - impala.impalad.mem_pool_total_bytes     # 被所有查询共享的内存池的大小
        - impala.impalad.mem_tracker_process_bytes_freed_by_last_gc # 上一次gc释放的内存
        - impala.impalad.mem_tracker_process_bytes_over_limit  #  上一次超过内存可用阈值的大小
        - impala.impalad.num_backends            # 与其他impala的后台连接数
        - impala.impalad.thrift_server_llama_callback_connections_rate  ## thrift_server_llama的链接速率
        - impala.impalad.thrift_server_llama_callback_connections_in_use ##活跃的thrift_server_llama回调连接数
        //- impala.impalad.resource_requests_released_rate  #still not
        //- impala.impalad.resource_requests_timedout_rate  #still not
        //- impala.impalad.resource_requests_rejected_rate  #still not
        - impala.impalad.tcmalloc_total_bytes_reserved  //预留给impalad的内存
        - impala.impalad.tcmalloc_physical_bytes_reserved //预留给impalad的物理内存
        - impala.impalad.tcmalloc_pageheap_unmapped_bytes //空闲未分配映射给page堆的内存
        - impala.impalad.tcmalloc_pageheap_free_bytes    //空闲page堆的内存
        - impala.impalad.tcmalloc_bytes_in_use          //正在使用的内存
        - impala.impalad.statestore_subscriber_statestore_client_cache_total_clients # 使用statestore缓存的客户端总数
        - impala.impalad.statestore_subscriber_statestore_client_cache_clients_in_use #使用statestore缓存的活跃客户端数量
        - impala.impalad.statestore_subscriber_last_recovery_duration       # statestore订阅的上次复原耗时
        - impala.impalad.statestore_subscriber_heartbeat_interval_time_stddev #statestore订阅的心跳时间标准差（平均值）
        - impala.impalad.statestore_subscriber_heartbeat_interval_time_rate #statestore订阅的心跳时间速率
        - impala.impalad.statestore_subscriber_heartbeat_interval_time_min  #statestore订阅的心跳时间最小值
        - impala.impalad.statestore_subscriber_heartbeat_interval_time_mean #statestore订阅的心跳时间平均值
        - impala.impalad.statestore_subscriber_heartbeat_interval_time_max  #statestore订阅的心跳时间最大值
        - impala.impalad.statestore_subscriber_heartbeat_interval_time_last #上一次statestore订阅的心跳时间
        - impala.impalad.scan_ranges_rate            #进程生存周期中的查询的速率
        - impala.impalad.scan_ranges_num_missing_volume_id_rate #进程生存周期中的没有元数据
        - impala.impalad.num_queries_rate            #进程生存周期中的中查询速率
        - impala.impalad.num_queries_expired_rate    #过期查询的速率
        - impala.impalad.num_sessions_expired_rate   #过期的会话速率
        - impala.impalad.thrift_server_backend_connections_rate  #后端thrift_server的链接速录
        - impala.impalad.thrift_server_backend_connections_in_use #后端thrift_server的活跃连接数
        //- impala.impalad.unexpected_exits_rate  #still not
        - impala.impalad.thrift_server_hiveserver2_frontend_connections_in_use #Hiveserver2的活跃连接数
        - impala.impalad.thrift_server_hiveserver2_frontend_connections_rate   #Hiveserver2的链接速率
        - impala.impalad.impala-server.ddl-durations-ms.25th     #impalad服务器耗时的前25%的耗时
        - impala.impalad.impala-server.ddl-durations-ms.50th    #impalad服务器耗时的前50%的耗时
        - impala.impalad.impala-server.ddl-durations-ms.75th    #impalad服务器耗时的前75%的耗时
        - impala.impalad.impala-server.ddl-durations-ms.90th    #impalad服务器耗时的前90%的耗时
        - impala.impalad.impala-server.ddl-durations-ms.95th    #impalad服务器耗时的前95%的耗时
        - impala.impalad.impala-server.ddl-durations-ms.99.9th  #impalad服务器耗时的前99.9%的耗时
        - impala.impalad.impala-server.ddl-durations-ms.count   #impalad服务器耗时的前25%的耗时


Hbase:
  Master:
    Hadoop:service=HBase,name=Master,sub=Server
        tag.liveRegionServers
        tag.deadRegionServers
        averageLoad
        numRegionServers
        numDeadRegionServers


  RegionServer:


    Hadoop:service=HBase,name=RegionServer,sub=Server
        totalRequestCount
        blockCacheFreeSize  #
        readRequestCount    #总读次数
        writeRequestCount   #总写次数
        flushedCellsCount   #
        flushedCellsSize    #flush到磁盘大小
        flushQueueLength    #
        blockedRequestCount #因memstore大于阈值而引发flush的次数
        slowGetCount        #请求完成时间超过1000ms的次数
        storeCount          #该Region Server管理的store个数
        mutationsWithoutWALCount
        mutationsWithoutWALSize
        blockCacheHitCount
        blockCacheMissCount


    Hadoop:service=HBase,name=RegionServer,sub=IPC：
        numActiveHandler   #RPC_handler的个数


    Hadoop:service=HBase,name=RegionServer,sub=WAL：
        slowAppendCount
        SyncTime_num_ops
        SyncTime_max
        SyncTime_mean
        AppendTime_num_ops
        AppendTime_max
        AppendTime_mean

HDFS:
  NameNode:
    FSSystemState
      VolumeFailure total
      NumStaleDataNodes
      NumStaleStorage

    FSNameSystem
      CorruptBlocks
      CapacityRemain
      NumLiveDataNode
      NumDeadDataNode
      Snapshot

    NameNodeInfo(mbean:Hadoop:service=NameNode,name=NameNodeInfo)
      Livenode


  DataNode:
    DataNodeActivity(mbean:Hadoop:service=DataNode,name=DataNodeActivity-$hostname)
      BlockVerificationFailures
      BlockReportsAvgTime
      BlockReportsNumOps
      HeartbeatsAvgTime
      HeartbeatsNumOps
      DatanodeNetworkErrors
      VolumeFailures
      ReplaceBlockOpNumOps
      ReplaceBlockOpAvgTime
    DataNodeInfo(mbean:Hadoop:service=DataNode,name=DataNodeInfo)
      DatanodeNetworkCounts




---------------------------
(yarn)MapReduce

- mapreduce.py
	# parse the configuration
	node = ResoucreManager
	hadoop.mapreduce.appsSubmitted 			int 	The number of applications submitted
	hadoop.mapreduce.appsCompleted 			int 	The number of applications completed
	hadoop.mapreduce.appsPending 			int	 	The number of applications pending
	hadoop.mapreduce.appsRunning 			int 	The number of applications running
	hadoop.mapreduce.appsFailed 			int	 	The number of applications failed
	hadoop.mapreduce.appsKilled 			int 	The number of applications killed
	hadoop.mapreduce.reservedMB 			long 	The amount of memory reserved in MB
	hadoop.mapreduce.availableMB 			long 	The amount of memory available in MB
	hadoop.mapreduce.allocatedMB 			long 	The amount of memory allocated in MB
	hadoop.mapreduce.totalMB 				long 	The amount of total memory in MB
	hadoop.mapreduce.reservedVirtualCores 	long 	The number of reserved virtual cores
	hadoop.mapreduce.availableVirtualCores 	long 	The number of available virtual cores
	hadoop.mapreduce.allocatedVirtualCores 	long 	The number of allocated virtual cores
	hadoop.mapreduce.totalVirtualCores 		long 	The total number of virtual cores
	hadoop.mapreduce.containersAllocated 	int 	The number of containers allocated
	hadoop.mapreduce.containersReserve 		int 	The number of containers reserved
	hadoop.mapreduce.containersPending 		int 	The number of containers pending
	hadoop.mapreduce.totalNodes 			int 	The total number of nodes
	hadoop.mapreduce.activeNodes 			int 	The number of active nodes
	hadoop.mapreduce.lostNodes 				int 	The number of lost nodes
	hadoop.mapreduce.unhealthyodes 			int 	The number of unhealthy nodes
	hadoop.mapreduce.decommissionedNodes 	int 	The number of nodes decommissioned
	hadoop.mapreduce.rebootedNodes 			int 	The number of nodes rebooted

- spark.py
    spark.application.counts 				int		attached tag: stauts[completed|running
	spark.application.duration              int(ms)     attached tag: status[completed|runnning], appId,

	---running applications only
	spark.application.taskComplRate         float   attached tag: appId,            hint: port 4040 ,real time data
	spark.application.activetask			int 	attached tag: appId, jobId
	spark.application.failedtask			int  	attached tag: appId, jobId
	spark.application.completedtask			int 	attached tag: appId, jobId

	---completed application only
	spark.executor.gctime					float   attached tag: appId, executorId
	spark.executor.duration					float   attached tag: appId, executorId



```



## Screenshots
Dashboard

![](./docs/img/Dashboard1.png)  
![](./docs/img/Dashboard2.png)  

Metric chart view

![](./docs/img/chartview.png)

Alert rules and messages:

![](./docs/img/alert1.png)
![](./docs/img/alert2.png)

Slack notification:

![](./docs/img/alert_notify_slack.jpeg)

Tracing display:

![](./docs/img/callchain1.png)  
![](./docs/img/callchain2.png)


## Architect
### Modules(corresponding repo)
- Web server: argus-web
- Backend:
    * Collector: argus_collector
    * Alert: argus_alert
    * Tracing: argus_chain
    * Statistics: argus_statistics
    * AIOps: argus_aiops


## Authors
Amas is maintained by [@Eacon](https://github.com/EaconTang) and his develop team, see more in [AUTHORS](AUTHORS).


## Other
* Amas' code name is "argus", and this would be reserved in source code.


## ToDoList:
- [ ] Support DSL defined rules in alert engine
- [ ] Integrate with Zabbix, Nagios...
- [ ] Java bytecode injection based on AspectJ
- [ ] Python bytecode injection based on pyrasite
- [ ] Landing more AIOps...

