# Amas

[![Docker Automated build](https://img.shields.io/docker/automated/jrottenberg/ffmpeg.svg)]()


选择语言: [English](README.md) | [中文](README_ch.md)

## Amas是什么
Amas是基于OpenTSDB开发的统一监控平台，为大数据平台而生，其特点包括：  
1. 覆盖大数据平台(Hadoop/Spark/HBase/Kakfa等)的常见监控指标
2. 采集器高度可扩展，支持不同脚本语言(Python/Perl/Shell/...)编写的的自定义采集指标
3. 基于HBase/OpenTSDB的海量数据存储架构，可快速读写大量监控指标
4. 清新简约的Web可视化界面，功能强大且易用
5. 分布式告警引擎，可水平扩展系统处理能力
6. 多渠道、可自定义的告警通知方式，自带微信、邮件以及Slack的实现
7. 基于OpenTracing的调用链路监控数据采集和展示
8. 支持docker部署运行
9. (More...)

## 项目成员
Amas现由[@Eacon](https://github.com/EaconTang)和他的开发团队负责维护, 详见[AUTHORS](AUTHORS).

## 技术栈
* 编程语言：Python, NodeJS
* Web服务：Vue, ECharts, Express
* 后台服务：
    - HBase, OpenTSDB, MongoDB, Redis
    - Spark, Kafka...
    - Jagger, Tornado
    - Docker, Swarm


## 服务端运行环境
* Linux(内核版本2.6+)
* Centos7(推荐)

## 其他说明
* Amas的内部开发代号为argus，这也会保留在开源项目的源码中。

<!--
## Docker快捷部署

1）如果你了解并安装了Docker，可以用以下命令一键运行，快速体验其界面功能：
```

```
2）如果你熟悉容器编排Docker-Compose，推荐使用以下方式运行：
```

``` -->
<!--

## 生产环境部署指南
 -->

## 部分功能截图
![](./docs/img/Dashboard1.png)  
![](./docs/img/Dashboard2.png)  
![](./docs/img/chartview.png)  
![](./docs/img/alert1.png)  
![](./docs/img/alert2.png)  
![](./docs/img/callchain1.png)  
![](./docs/img/callchain2.png)  


<!-- ## 技术架构 -->
