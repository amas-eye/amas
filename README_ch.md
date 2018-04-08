# Amas

[![Docker Automated build](https://img.shields.io/docker/automated/jrottenberg/ffmpeg.svg)](https://hub.docker.com/u/eacon/)

Language: [English](README.md) | [中文](README_ch.md)


## Amas是什么
Amas是基于大数据平台技术开发的统一监控平台，其特点包括：
1. 全维度监控指标，覆盖从操作系统、中间件、大数据平台(Hadoop/Spark/HBase/Kakfa等)到代码级别
2. 可扩展、自定义的采集框架，支持不同语言(Python/Perl/Shell/...)开发的采集器
3. 基于OpenTSDB/HBase的海量数据存储架构，可快速读写大量监控指标，满足真实生产环境
4. 清新简约的Web界面，功能强大但简单易用
5. 基于Python原生multiprocess和async/await实现的分布式异步告警引擎，可水平扩展系统处理能力
6. 多渠道、可自定义的通知方式(微信/邮件/Slack/API...)
7. 可分组聚合的告警信息，避免海量数据监控场景下的告警风暴
8. 基于Jagger的分布式链路追踪数据提取和展示，历史事件可追溯
9. 可对接基于机器学习的异常检测服务，落地AIOps智能运维
10. 微服务架构，支持docker和docker-compose方式的部署
11. ...


## 技术栈
* 编程语言：
    - (Backend)Python
    - (Web)Javascript
* Web服务：
    - Vue, ECharts, Webpack
    - Express(NodeJS)
* 后台服务：
    - HBase, OpenTSDB, MongoDB, Redis
    - Spark, Kafka...
    - Jagger, Tornado
    - Pandas, Scikit-learn
    - Docker, Swarm


## 服务端运行环境
* Linux(内核版本2.6+)
* Centos7(推荐)


## Docker快速部署
目前Amas的代码已经通过DockerHub实现自动构建，推荐使用docker来快速体验：
1. 安装docker
2. 保存如下shell脚本并执行：
```bash
#!/usr/bin/env bash

# 创建docker网络
docker network create amas

# 运行数据库服务
# opentsdb(v2.3.0+)
# mongo(v3.10.0+)
# redis(v3.10.0+)
docker run -d -p 4242:4242 --name opentsdb --network amas eacon/docker-opentsdb
docker run -d -p 27017:27017 --name mongo --network amas mongo
docker run -d -p 6379:6379 --name redis --network amas redis

# 运行采集Agent（含Agent Manager）：
docker run -d --name collector --network amas -p 8001:8001 eacon/argus_collector

# 运行告警模块：
docker run -d --name alert --network amas eacon/argus_alert

# 运行统计模块：
docker run -d --name statistics --network amas eacon/argus_statistics

# 运行Web服务：
docker run -d --name web --network amas -p 8080:8080 eacon/argus-web
```
3. 访问界面：本地8080端口（通过```127.0.0.1```而不是```localhost```）：[http://127.0.0.1:8080](http://127.0.0.1:8080)
4. 初始化：执行web容器的命令，初始化默认账户（用户名/密码：admin/123）：
```
docker exec -it web init_user
```

### Docker-Compose
如果你使用了docker-compose，可以通过如下方式快速运行：
1. git clone本仓库：
```
git clone https://github.com/amas-eye/amas.git; cd amas/docker/compose/
```
- 或者直接获取文件：
```
mkdir amas; cd amas; curl https://raw.githubusercontent.com/amas-eye/amas/master/docker/compose/docker-compose.yml > docker-compose.yml
```
2. 执行：
```
docker-compose up -d
```


<!-- ## 生产环境部署指南 -->
<!-- （更新中） -->

## 指标说明
详见 [Metrics.md](./docs/dev/argus_collector/Metrics.md)。


## 部分功能截图
Dashboard

![](./docs/img/Dashboard1.png)
![](./docs/img/Dashboard2.png)

监控图表

![](./docs/img/chartview.png)

告警规则和记录

![](./docs/img/alert1.png)
![](./docs/img/alert2.png)

Slack通知

![](./docs/img/alert_notify_slack.jpeg)

调用链

![](./docs/img/callchain1.png)
![](./docs/img/callchain2.png)




## 架构
### 模块划分(对应repo)
- Web服务：argus-web
- 后台：
    * 采集器：argus_collector
    * 告警：argus_alert
    * 调用链：argus_chain
    * 统计中心：argus_statistics
    * AIOps框架：argus_aiops

<!-- ### 架构图 -->





## 项目成员
Amas现由[@Eacon](https://github.com/EaconTang)和他的开发团队负责维护, 详见[AUTHORS](AUTHORS).


## 其他
* Amas的内部开发代号为argus，这也会保留在开源项目的源码中。


## ToDoList

- [ ] 告警引擎，支持DSL语言定义规则
- [ ] 集成开源的Zabbix、Nagios等监控数据
- [ ] 基于AspectJ的Java字节码注入监控
- [ ] 基于pyrasite的python字节码注入监控
- [ ] 更多AIOps方案的落地...