#!/usr/bin/env python
# -*- coding: utf-8 -*-
#     Filename @  spark_conf.py
#       Author @  gouhao
#  Create date @  2017-07-28

"""
The LAST_TIME_PATH is the middle file used to record the last completed  application finished time. 
First collection should run a long time due to default last time is null
which make the collector to fetch the whole application records
"""
import os

SPARK_HOST = 'localhost'
SPARK_RUNNING_PORT = 4040

SPARK_HISTORY_SERVER_HOST = 'localhost'
SPARK_HISTORY_SERVER_PORT = 18080


# 2017-08-04T03:20:50.804GMT ---> 时间格式
LAST_TIME_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/data/spark.data'

# COMPLETED_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) +'/data/COMPLETED.log'
# RUNNING_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) +'/data/RUNNING.log'

# spark_config_path = '/root/spark-2.2.0-bin-hadoop2.7/conf/'
