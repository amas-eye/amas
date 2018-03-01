# 首页服务部署文档

这个服务是要与argus-web一起进行部署，需要公用一个数据库host,并且需要读取集群中的opentsdb进行部分数据的获取
运行环境为python3(>=3.6.0)，建议使用虚拟环境进行部署，虚拟环境建议使用包为venv 或者virtualenvwrapper


## 部署方法：
1. pip install -r requirements
2. 修改settings.py配置文件
3. 启动程序
   1. 方法一 （直接使用nohup进行启动）
    ```
     nohup python start_dashboard.py --start &
    ```
   2. 方法二 使用supervisor进行启动，详情根据supervisor官方文档进行配置
