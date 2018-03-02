# coding=utf-8
"""Slave进程

1）从manager的队列拿到task后，置入本地任务池中
2) 起线程池或者协程池，并发消费任务池的告警任务
    2.1）每一类特定的告警策略，需要有对应的任务处理实现，消费者只需要调用统一的方法进行处理即可
    2.2）以基本告警为例，一般的处理流程包括：
        2.2.1) 根据策略字段，构造请求tsd的url
        2.2.2）查询结果后，比对阈值，并将结果记录到redis
        2.2.3) 如果结果触发了告警通知（如：主要是alert都进行通知/状态发送变化才通知），将告警内容发送到通知处理队列

"""
import asyncio
import time
from queue import Queue, Empty
from threading import Thread

from pymongo import MongoClient
from redis import Redis

from argus_alert.core.inspect.strategy_handler import run_alert_task
from argus_alert.core.utils.log import timed_logger
from argus_alert.etc.bootstrap import RunningConfig

LOG = timed_logger()


class ExecutorProcess(object):
    def __init__(self, task_queue, redis_addr, mongo_addr, tsd_addr):
        self._remote_q = task_queue
        self._local_q = Queue()
        self._redis_addr = redis_addr
        self._redis_client = None
        self._mongo_addr = mongo_addr
        self._mongo_client = None
        self._tsd_addr = tsd_addr
        self._tsd_pool = None  # TODO
        self._event_loop = asyncio.get_event_loop()
        self.q_get_timeout = 10
        self.q_empty_sleep = 10

    @property
    def redis_client(self):
        '''
        get a redis client to record and push alert to notifier
        '''
        if not self._redis_client:
            self._redis_client = Redis.from_url(self._redis_addr, decode_response=True)
        return self._redis_client

    @property
    def mongo_client(self):
        '''
        get a mongo client to connect to the mongodb to read strategy
        '''
        if not self._mongo_client:
            self._mongo_client = MongoClient(self._mongo_addr)
        return self._mongo_client

    def receiver_sentinel(self):
        """
        负责从远程队列接收task的线程，并置入本地队列
        get task item from remote queue(python remote queue),
        """
        while True:
            try:
                item = self._remote_q.get(timeout=self.q_get_timeout)
                LOG.debug(f'Executor got task, time: {item["task_time"]}, '
                          f'ObjectId: {item["strategy"]["_id"]}, strategy_name: {item["strategy"]["property"]["name"]}')
                self._local_q.put(item)
            except Empty:
                # LOG.debug('No task from driver, try again after {} seconds.'.format(self.q_empty_sleep))
                time.sleep(self.q_empty_sleep)
                continue
            except EOFError:
                print('Could not read from driver, exit...')
                break

    def queue_sentinel(self):
        """
        统计本地队列大小
        To calculat local queue size 
        """
        LOG.info('start local queue sentinel...')
        while True:
            time.sleep(5)
            # LOG.debug('Local queue size now: {}'.format(self._local_q.qsize()))

    # async def _consume_task(self):
    #     """处理任务的协程"""
    #     while True:
    #         try:
    #             item = self._local_q.get_nowait()
    #         except Empty:
    #             print('No task to do, try again after {} seconds.'.format(self.q_empty_sleep))
    #             await asyncio.sleep(self.q_empty_sleep)
    #             continue
    #         else:
    #             await run_alert_task(item['strategy_dict'], timestamp=item['time'],
    #                                  tsd_addr=self._tsd_addr, redis_addr=self._redis_addr)
    #             print('task is done.')
    #
    # def run_loop(self):
    #     """"""
    #     tasks = [self._consume_task() for _ in range(RunningConfig.SLAVE_COROUTINES)]
    #     print('Starting slave event loop...')
    #     self._event_loop.run_until_complete(asyncio.wait(tasks))
    #

    def consume_task(self):
        """
        处理任务的线程
        The Thread to handler strategy_task 
        """
        while True:
            try:
                item = self._local_q.get_nowait()
            except Empty:
                # LOG.warn('No task to do, try again after {} seconds.'.format(self.q_empty_sleep))
                time.sleep(self.q_empty_sleep)
                continue
            else:
                ctx = dict(strategy=item['strategy'],
                           task_time=item['task_time'],
                           tsd_addr=self._tsd_addr,
                           redis_addr=self._redis_addr,
                           mongo_addr=self._mongo_addr)
                run_alert_task(ctx)
                LOG.debug('task done.')

    def run(self):
        """
        Try to run the exector
        """
        Thread(target=self.receiver_sentinel, name='receiver').start()
        Thread(target=self.queue_sentinel, name='queue_sentinel').start()
        consumers = [Thread(target=self.consume_task, name=f'consumer-{n}') for n in
                     range(RunningConfig.EXECUTOR_THREADS)]
        for consumer in consumers:
            consumer.start()
        # for consumer in consumers:
        #     consumer.join()


if __name__ == '__main__':
    pass

    from argus_alert.core.inspect.manager import ExecutorManager

    em = ExecutorManager()
    em.start()


    # from argus_alert.core.inspect.manager import TaskSlave
    #
    # slaves = [TaskSlave(tsd_addr='localhost:4242') for _ in range(RunningConfig.SLAVE_WORKER)]
    # for s in slaves:
    #     s.start()

    # from random import randint
    #
    # def foo(n):
    #     time.sleep(n + randint(1, 5))
    #     print('done ', n)
    #
    # with ThreadPoolExecutor(max_workers=5, thread_name_prefix='slave-') as exe:
    #     # exe.map(foo, [1,2,3,4,5])
    #     for _ in range(5):
    #         exe.submit(foo, (_,))
    #
    # print('hah')
