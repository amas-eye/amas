# coding=utf-8
"""Driver进程

1）从mongodb加载告警策略，一个策略一个协程，根据告警检查间隔定时投入告警任务到任务池
2）定时更新：
    1）启动时会加载所有告警策略
    2）如果mongo中的告警策略有变化（增删策略/修改字段），将重建生产告警任务的线程
    3）mongo中策略是否变化，可以由单独的线程定期检查，或者提供接口主动触发检查

"""
import time
import asyncio
import json
import copy
from threading import Thread
from queue import Full

from pymongo import MongoClient
from redis import Redis
import aioredis
from argus_alert.core.utils.common import decode_utf8
from argus_alert.core.rest.status_code import *
from argus_alert.core.utils.log import timed_logger
from bson.objectid import ObjectId

LOG = timed_logger()


class DriverProcess(object):
    def __init__(self, task_queue, redis_addr, mongo_addr):
        self._task_q = task_queue
        self._mongo_addr = mongo_addr
        self._mongo_client = None
        self._redis_addr = redis_addr
        self._redis_client = None
        self._aio_redis_client = None
        self._strategys = []
        self._id_strategy_dict = {}
        self._event_loop = None
        self._default_interval = 5 * 60
        self._update_dict = {}

    @property
    def event_loop(self):
        if self._event_loop is None:
            self._event_loop = asyncio.get_event_loop()
        return self._event_loop

    @property
    def mongo_client(self):
        if not self._mongo_client:
            self._mongo_client = MongoClient(self._mongo_addr)
        return self._mongo_client

    @property
    def redis_client(self):
        if not self._redis_client:
            self._redis_client = Redis.from_url(self._redis_addr, decode_response=True)
        return self._redis_client

    async def get_aioredis_client(self):
        if not self._aio_redis_client:
            self._aio_redis_client = await aioredis.create_redis('redis://localhost')
            # LOG('aio_redis_client create done')
            rebuild_channel = await self._aio_redis_client.subscribe('rebuild_strategy')
            self.rebuild_channel = rebuild_channel[0]
            LOG.debug("rebuild_channel")
            LOG.debug(self.rebuild_channel)
            LOG.debug(type(self.rebuild_channel))

    @property
    def strategys(self):
        """告警策略列表"""
        if not self._strategys:
            self._strategys = [_ for _ in \
                               self.mongo_client['argus-alert']['strategy'].find({'status': {'$in': ['ok', 'alert']}})]
            LOG.info('Strategys loaded.')
            LOG.debug('Strategys: {}'.format(self._strategys))
        return self._strategys

    def queue_sentinel(self):
        """定时统计driver进程的任务队列大小(到redis/tsd)，监控队列积压情况"""
        LOG.info('start queue sentinel...')
        while True:
            try:
                time.sleep(5)
                qsize = self._task_q.qsize()
                # LOG.debug(f'Task queue size now: {qsize}')
                # TODO: 发送到redis或tsd
            except EOFError:
                LOG.warn('the queue is no task putting in')

    def create_strategy(self, cid):
         """
         把新的策略添加到事件循环当中
         """
         Oid = ObjectId(cid)
         strategy_cursor = self.mongo_client['argus-alert']['strategy'].find({"_id": Oid})
         new_strategys = [item for item in strategy_cursor]
         new_strategy = copy.deepcopy(new_strategys[0])
         del(new_strategys)
         self._strategys.append(new_strategy)
         asyncio.ensure_future(self.produce_task(new_strategy))
         #  self.event_loop.call_soon(self.produce_task, (new_stratygy))


    def detele_strategy(self, did):
        """
        把策略从strategy属性中删除，在下一次执行这个策略的时候进行判断，然后把那个coroutine退出
        """
        Oid = ObjectId(did)
        count = 0
        for strategy in self._strategys:
            if strategy['_id'] == Oid:
                del (self._strategys[count])
                LOG.debug('strategy delete')
                break
            count += 1

    def update_single_strategy(self, uid):
        self._update_dict[uid] = 1

    async def redis_cmd(self, channel):
        """
        处理单条策略的更新，异步读取Redis，然后进行处理。信道传输对象为Json{$action:strategy_id}
        如{'del':strategy_id}
        action == ('update' | 'del' | 'create')
        """
        while True:
            msg = await channel.get(encoding='utf-8')
            LOG.debug(f"got msg in pubsub {msg}")
            LOG.debug('rebuild msg receive, rebuilding')
            # self.rebuild_loop()
            LOG.debug(f'msg is {msg}')
            msg = json.loads(msg)
            type_msg = type(msg)
            LOG.debug(f'msg is {msg}')
            LOG.debug(f'msg type {type_msg}')
            for key in msg.keys():
                LOG.debug(f'msg key is {key}')
                if key == 'del':
                    del_id = msg[key]
                    LOG.debug(f'delete id is {del_id}')
                    self.detele_strategy(del_id)
                elif key == "create":
                    create_id = msg[key]
                    self.create_strategy(create_id)
                elif key == "update":
                    update_id = msg[key]
                    self.update_single_strategy(update_id)

    async def produce_task(self, strategy):
        """产生任务并异步投入队列"""
        while True:
            task_time = int(time.time())
            item = dict(task_time=task_time, strategy=strategy)
            exist_status = 0
            while True:
                try:
                    i = strategy['_id']
                    ti = type(strategy['_id'])
                    str_id = str(strategy["_id"])
                    t_str_id = type(str_id)
                    LOG.debug(f'strategy_id type {ti} is in produce_task')
                    LOG.debug(f'strategy_id {i} is in produce_task')
                    LOG.debug(f'strategy_id  str {str_id} is in produce_task')
                    LOG.debug(f'strategy_id  type {t_str_id} is in produce_task')
                    k = list(self._update_dict.keys())
                    LOG.debug(f'key in update dict {k}')
                    result = (str_id in k)
                    LOG.debug(f'result is {result}')
                    if str_id in k:
                        LOG.debug('in update process')
                        new_strategy = [i for i in self.mongo_client['argus-alert']['strategy'].find({"_id": i})]
                        LOG.debug(f'new _strategy is {new_strategy}')
                        strategy = new_strategy[0]
                        item = dict(task_time=task_time, strategy=strategy)
                        LOG.debug(f'strategy is _update, {strategy}')
                        del (self._update_dict[str_id])
                        LOG.debug(self._update_dict)
                        self._strategys.append(new_strategy[0])
                    if strategy in self._strategys:
                        self._task_q.put_nowait(item)
                        LOG.debug(
                            f'Driver put task, time: {item["task_time"]}, '
                            f'ObjectId: {strategy["_id"]}, strategy_name: {strategy["property"]["name"]}')
                    else:
                        exist_status = 1
                except Full:
                    LOG.warn('Task queue no free slot available! Try after 5s...')
                    await asyncio.sleep(5)
                except EOFError:
                    LOG.warn('Production Coroutine done , wait new task put in')
                else:
                    break
            if not exist_status:
                await asyncio.sleep(int(strategy.get('interval', self._default_interval)))
            else:
                LOG.warn(f'the strategy has been delete ,id is {strategy["_id"]}')
                break

    # def reload_sentinel(self):
    #     """事件循环的重启操作，通过监听redis中的发送cmd:reload_strategy的channel"""
    #     # TODO：待重构
    #     pubsub = self.redis_client.pubsub(ignore_subscribe_messages=True)
    #     pubsub.subscribe(CHANNEL_CMD_RELOAD_STRATEGY)
    #     while True:
    #         time.sleep(1)
    #         # get_message() uses the system’s ‘select’ module to quickly poll the connection’s socket
    #         msg = pubsub.get_message()
    #         if msg is not None:
    #             print('Got msg: ', msg)
    #             if decode_utf8(msg['data']) == CMD_RELOAD_STRATEGY:
    #                 print('Got cmd: ', CMD_RELOAD_STRATEGY)
    #                 self.reload_strategy()

    # def reload_strategy(self):
    #     """重新载入告警策略"""
    #     # TODO：待重构
    #     # make use of @property，just set to None and they would restore themselves
    #     self._strategys, self._id_strategy_dict = None, None
    #     self.rebuild_loop()

    def run_loop(self):
        """生成任务的协程的事件循环"""
        # channel = await self.aioredis_client()
        self.event_loop.run_until_complete(self.get_aioredis_client())
        LOG.debug(self.rebuild_channel)
        LOG.debug(dir(self.rebuild_channel))
        LOG.debug(self.rebuild_channel.is_active)
        tasks = [self.produce_task(strategy) for strategy in self.strategys]
        tasks.append(self.redis_cmd(self.rebuild_channel))
        if tasks:
            LOG.debug('starting event loop...')
            # self.event_loop.run_until_complete(asyncio.wait(tasks))
            # self.event_loop.run_until_complete(asyncio.wait(tasks))
            for task in tasks:
                asyncio.ensure_future(task)
            self.event_loop.run_forever()

    # def exit_loop(self):
    #     """退出事件循环"""
    #     try:
    #         # TODO: how to close gracefully
    #         self._event_loop.shutdown_asyncgens()
    #         self._event_loop.stop()
    #         self._event_loop.close()
    #     except:
    #         pass
    #     print('Exit event loop.')
    #     print('loop closed? ', self._event_loop.is_closed())

    # def rebuild_loop(self):
    #     """重建整个事件循环"""
    #     self.exit_loop()
    #     new_loop = asyncio.new_event_loop()
    #     asyncio.set_event_loop(new_loop)
    #     self._event_loop = None
    #     Thread(target=self.reload_sentinel).start()
    #     self.run_loop()

    def run(self):
        """主入口"""
        Thread(target=self.queue_sentinel, name='queue_sentinel').start()
        # TODO: 定时更新策略的线程，待重构, 采用signal信号捕捉？
        # Thread(target=self.reload_sentinel).start()
        self.run_loop()


if __name__ == '__main__':
    from queue import Queue

    # dp = DriverProcess(
    #     task_queue=Queue(),
    #     redis_addr='redis:///@localhost:6379/0',
    #     mongo_addr='mongodb://10.17.35.43:27017/'
    # )
    # dp.run()
    #
    #

    from argus_alert.core.inspect.manager import DriverManager

    dm = DriverManager()
    dm.start()
