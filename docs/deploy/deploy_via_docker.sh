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