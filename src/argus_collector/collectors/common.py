# coding=utf-8
"""
采集器脚本公共方法
"""
import json
import os
import time
import functools

from argus_collector.conf.settings import BASE_DIR

DATA_DIR = os.path.join(BASE_DIR, 'collectors', 'data')


def get_last_data(pathfile):
    """获取上次脚本运行保存的数据"""
    if not os.path.exists(pathfile):
        return None
    with open(pathfile) as f:
        data_str = f.read()
        if not data_str.strip():
            return None
        else:
            return json.loads(data_str)


def save_data(pathfile, data, timestamp=None):
    """保存(更新)数据到json文件，并记录时间戳"""
    if timestamp is None:
        timestamp = int(time.time())
    with open(pathfile, 'w') as f:
        json.dump({timestamp: data}, f, indent=2)


def cache(func):
    """缓存装饰器，如果函数或类的名和参数相同，返回之前保存的结果"""
    _cached = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 检查是否_instances的key；如果是，直接返回之前的结果
        key = '<{0}_{1}_{2}>'.format(func.__name__, args, kwargs)
        if key not in _cached:
            _cached[key] = func(*args, **kwargs)
        return _cached[key]

    return wrapper