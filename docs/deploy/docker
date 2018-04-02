# Docker部署方式

## Docker运行
1. 安装docker
2. 依次执行如下命令，或者保存为shell脚本执行：
```
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

## 访问界面
- 访问本地8080端口（通过```127.0.0.1```而不是```localhost```）：[http://127.0.0.1:8080](http://127.0.0.1:8080)


## 初始化
- 执行web容器的命令，初始化默认账户（用户名/密码：admin/123）：
```
docker exec -it web init_user
```


## Docker-Compose编排运行
1. 安装docker和docker-compose
2. 拉取compose文件，cd到文件所在目录并运行:
```docker-compose up -d```
