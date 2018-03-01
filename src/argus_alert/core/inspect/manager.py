# coding=utf-8
"""分布式服务进程

1）Driver负责拉取告警策略、定时生成任务到队列
2）分布式进程Executor连接Driver网络端口，获取任务并进行处理
3）所有告警策略的最新状态存储到redis
4）Driver启动multiprocessing.manager并暴露在网络端口，生成task到队列，Executor从队列获取task并处理

并发考虑：
1）redis-py客户端自动维护连接池，且线程安全
2）告警策略过多，意味着线程数也会过多，可能受文件资源限制，采用协程这种用户态线程应该可以避免
3）mongo客户端连接池

"""
import queue
import time
from multiprocessing import Process
from multiprocessing.managers import BaseManager
from collections import namedtuple

from argus_alert.core.inspect.driver import DriverProcess
from argus_alert.core.inspect.executor import ExecutorProcess
from argus_alert.etc.bootstrap import RunningConfig
from argus_alert.core.utils.log import timed_logger

LOG = timed_logger()


class _TaskManager(BaseManager): pass


task_queue = queue.Queue()
priority_task_queue = queue.PriorityQueue()     # 带优先级的告警任务队列

# 注册管理器的方法
_TaskManager.register('get_task_queue', callable=lambda: task_queue)
_TaskManager.register('get_priority_task_queue', callable=lambda: priority_task_queue)


class DriverManager(object):
    """Driver管理进程"""

    def __init__(self, host='', port=7001, authkey='',
                 redis_addr='redis:///@localhost:6379/0',
                 mongo_addr='mongodb://localhost:27017/'):
        self.host = host
        self.port = port
        self.authkey = bytes(authkey, encoding='utf-8')
        self.redis_addr = redis_addr
        self.mongo_addr = mongo_addr
        self.manager = _TaskManager(address=(host, port), authkey=self.authkey)
        self.manager.start()
        LOG.info(f'Driver manager started, listening on {host}:{port}')
        self.task_queue = self.manager.get_task_queue()
        self.priority_task_queue = self.manager.get_priority_task_queue()

    def start(self):
        driver = DriverProcess(task_queue=self.task_queue,
                               redis_addr=self.redis_addr,
                               mongo_addr=self.mongo_addr)
        driver.run()

    def close(self):
        self.manager.shutdown()
        LOG.info('Driver manager exit.')


class ExecutorManager(Process):
    """Executor管理进程,启动时候需要把对应的数据库位置进行修改"""
    def __init__(self, host='localhost', port=7001, authkey='',
                 redis_addr='redis:///@localhost:6379/0',
                 mongo_addr='mongodb://localhost:27017/',
                 tsd_addr='localhost:4242',
                 **kwargs):
        Process.__init__(self, **kwargs)
        self.host = host
        self.port = port
        self.authkey = bytes(authkey, encoding='utf8')
        self.redis_addr = redis_addr
        self.mongo_addr = mongo_addr
        self.tsd_addr = tsd_addr
        self.manager = _TaskManager(address=(host, port), authkey=self.authkey)

    def start(self):
        try:
            self.manager.connect()
        except ConnectionRefusedError:
            LOG.error('Manager refused connection, exit...')
            self.close()
            return
        LOG.info('Executor connected to: {}'.format(self.manager._address))
        remote_task_queue = self.manager.get_task_queue()
        slave = ExecutorProcess(task_queue=remote_task_queue,
                                redis_addr=self.redis_addr,
                                mongo_addr=self.mongo_addr,
                                tsd_addr=self.tsd_addr)
        slave.run()


    def close(self):
        self.manager.shutdown()
        LOG.info('Executor exit.')


if __name__ == '__main__':
    pass


