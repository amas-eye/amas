# argus-statistics

## 这个模块是用于处理展示在dashboard的函数


### 使用方法
####启动
nohup python start_dashboard.py --start & 
####重启
nohup python start_dashboard.py --restart \& 
####停止
nohup python start_dashboard.py --stop & 


### host_stat 和 overall_health 共用一个配置文件[host_config.json]
- 配置项：
  - host_total_num :配置所有存在的主机数（如果为空，我们通过通用采集器进行统计）
  - manage_host: 用于连接采集管理机器的IP
  - manget_port: 用于连接采集管理机器的端口
  - alive_interval: 用于判断机器是否关闭的时间，大于此时间即为关闭(默认时间为1h)
  
### 更新频率
更新频率可以通过对配置文件中的update_config.json中"update_interval"进行修改
默认更新频率为5分钟，默认单位为分钟，假如想以小时为更新单位，应该写为 n*60(n为小时数)

###入口文件为 start_dashboard.py
使用方法:<br>
python start_dashboard.py --start/stop/restart <br>
来分别进行启动，停止和重启这个更新dashboard数据的模块

数据统计模块，主要用于Dashboard界面的数据展示

**产品一期Dashboard, 更新时间 09/13/2017**

**前端只能读取数据、不能执行写操作, Mock请使用测试数据库（自行处理)**


MongoDB   10.17.35.43:27017 测试

OpenTSDB  10.17.35.43:4242 测试

1. 健康度 -> Mongo.argus-statistics.overall_health
2. 主机 -> Mongo.argus-statistics.host_stat
3. 告警 -> Mongo.argus-statistics.alert_stat
4. 指标 -> Mongo.argus-statistics.metric_stat
5. 告警趋势 -> Mongo.argus-statistic.alert_trend
5. 所有Top5及基础资源使用量 -> Mongo.argus-statistics.sys_resource
6. 网络流入/流出趋势, 大数据指标概览 -> OpenTSDB.api

**Mongo中所有数据字段已做到见名知义**

**OpenTSDB访问方式如下**


[OpenTSDB时序数据库](https://opentsdb.net)

> {host}:{port}/api/query?start={start_time}&m=sum:{metric_name:待定}

> e.g. /api/query?start=5m-ago&m=sum:cluster.net.dev.receive 流入

> e.g. /api/query?start=5m-ago&m=sum:cluster.net.dev.transmit 流出

start_time可设置为UNIX时间戳或以当前时间为标准多久以前

1. 1505292683.5504668（支持毫秒级）
2. {十进制整数}{单位 s: 秒， m: 分钟， d: 天}-ago e.g. 5d-ago:5天前