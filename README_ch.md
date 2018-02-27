# Amas-Eye

[![Docker Automated build](https://img.shields.io/docker/automated/jrottenberg/ffmpeg.svg)]()

选择语言: [English](README.md) | [中文](README_ch.md)

## Amas-Eye是什么
Amas 是“Amas, monitor alert system”的递归首字母缩写。  
Amas是基于OpenTSDB开发的统一监控平台，其特点包括如下：
1. 覆盖大数据平台(Hadoop/Spark/HBase/Kakfa等)的常见监控指标
2. 采集器高度可扩展，支持不同脚本语言(Python/Perl/Shell/...)编写的的自定义采集指标
3. 基于HBase/OpenTSDB的海量数据存储架构，可快速读写大量监控指标
4. 独立开发的Web可视化界面，功能强大
5. 独立开发的告警引擎，可水平扩展告警处理能力
6. 基于OpenTracing的调用链路监控数据采集和展示
7. 支持docker部署运行
7. (More...)


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
![](./docs/img/(Dashboard1.png)
![](./docs/img/(Dashboard2.png)
![](./docs/img/(chartview.png)
![](./docs/img/(alert1.png)
![](./docs/img/(alert2.png)
![](./docs/img/(callchain1.png)
![](./docs/img/(callchain2.png)


<!-- ## 技术架构 -->
