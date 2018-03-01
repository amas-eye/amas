# 部署文档


## Python
- 请使用Python3.6以上的版本进行程序的运行

## 数据库依赖
0. mongodb version>=3.4.0
1. redis version>= 3.10.0
2. opentsdb version>=2.3.0

## 设置环境变量

    

##python 运行环境
我们强烈建议使用虚拟环境来运行此服务，以免依赖对系统自带python的污染
我们建议使用的虚拟环境包为virtualenvwrapper，详情可以查看
https://virtualenvwrapper.readthedocs.io/en/latest/

## 部署步骤
0. 设置PYTHONPATH环境变量
    ```
    在/etc/profile 或者~/.bashrc下面进行修改
       exprot ARGUS_ALERT=<path/to/argus-alert>
       export PYTHONPATH=$PYTHONPATH:$ARGUS_ALERT
    ```

1. 安装依赖
    cd $ARGUS_ALERT/argus_alert/libs && pip3 install -r requirements.txt


2.运行

   <!-- cd $ARGUS_ALERT/argus_alert/bin && ./start-local.py -->
   ### 使用supervisor进行启动
   1. 使用python2，创建一个虚拟环境， 然后 pip install supervisor
   2. 修改supervisord.conf
      修改部分为：
      [program:driver] | [program:exector] | [program:notifier]中的
      directory 修改为 实际环境中程序的存放路径
      如果使用python3的虚拟环境解释器进行对程序的启动，需要把python3改为对应python3的虚拟环境的可执行python程序
      [supervisord部分]，可以查看http://www.supervisord.org/，进行详细的修改
   3. 启动程序 
      ```
       supervisord -c supervisor.conf
      ``` 

   ### 单独启动
   1. nohup python3 argus-alert/argus_alert/core/inspect/driver.py &
   2. nohup python3 argus-alert/argus_alert/core/inspect/exector.py &
   3. nohup python3 argus-alert/argus_alert/core/notice/handler.py &