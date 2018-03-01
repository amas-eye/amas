# coding=utf-8
"""各种告警策略处理逻辑的具体实现

1）Executor从远程队列获取任务，将任务内容等上下文信息传入run_alert_task方法
2）根据告警类型，选择相应的handler处理告警策略
3）handler（已注册）调用run方法处理，判断是否产生告警通知；如果有，投入到redis队列
4）handler更新对应策略的最新状态，保存到redis
5）redis中，对应的key为：
        strategy:{strategy_id}:state
        strategy:{strategy_id}:{group_str}:state
   strategy_id即mongo的ObjectId，group即分组的tag(eg. "host=web01")
   对应的value是json字符串，反序列化后的字典结构为：
        strategy:{strategy_id}:state
            - status
            - timestamp
            - group_keys
            - info (option)
                当只有一个group时，该group的info作为整个strategy的info
        strategy:{strategy_id}:{group}:state
            - status
            - timestamp
            - info

"""
from functools import wraps
from time import time
import asyncio
import json
from ast import literal_eval
from abc import ABCMeta, abstractmethod, abstractproperty

import requests
from redis import Redis, ConnectionPool
from pymongo import MongoClient
from bson.objectid import ObjectId


from argus_alert.core.utils.log import timed_logger

LOG = timed_logger()
HandlerDict = {}


def run_alert_task(ctx):
    """根据告警类型type，选择相应的对象进行处理"""
    alert_type = ctx['strategy'].get('type', 'basic')
    try:
        Handler = HandlerDict.get(alert_type.upper())
    except KeyError:
        LOG.error(f'No handler found for alert, type: {alert_type}')
    else:
        Handler(ctx).run()


def register_handler(cls):
    """将告警策略处理对象注册到全局字典中，可作为装饰器使用
       （使用子类查找也可以实现，但不够优雅和安全）
    """
    if cls.TYPE not in HandlerDict:
        HandlerDict[cls.TYPE.upper()] = cls

    @wraps(cls)
    def _handler(*args, **kwargs):
        return cls(*args, **kwargs)

    return _handler


STATUS_OK = 'OK'
STATUS_ALERT = 'ALERT'


class IHandler(object):
    """告警任务处理的基类
    新实现的告警需要继承、实现run()方法和定义TYPE属性（即策略表中的type字段），并注册到字典中
    上下文对象可用的属性包括：
        self.ctx
            - strategy
            - task_time
            - tsd_addr
            - redis_addr
            - mongo_addr
            - redis_cli
            - mongo_cli
    """
    __metaclass__ = ABCMeta
    TYPE = '__base__'

    def __init__(self, ctx=None):
        self.ctx = ctx
        self.strategy = self.ctx['strategy']
        self.task_time = self.ctx['task_time']
        self.tsd_addr = self.ctx['tsd_addr']
        self.redis_addr = self.ctx['redis_addr']
        self.mongo_addr = self.ctx['mongo_addr']
        self._redis_client = None
        self._redis_pool = None
        self._mongo_client = None

    @property
    def redis_cli(self):
        if not self._redis_client:
            self._redis_client = Redis(connection_pool=self.redis_pool, decode_responses=True)
        return self._redis_client

    @property
    def redis_pool(self):
        if not self._redis_pool:
            self._redis_pool = ConnectionPool.from_url(self.redis_addr)
        return self._redis_pool

    @property
    def mongo_cli(self):
        if not self._mongo_client:
            self._mongo_client = MongoClient(self.mongo_addr)
        return self._mongo_client

    @staticmethod
    def unit_to_seconds(unit):
        """时间单位转换"""
        return {
            's': 1,
            'm': 60,
            'h': 60 * 60,
            'd': 60 * 60 * 24,
            'w': 60 * 60 * 24 * 7,
            'n': 60 * 60 * 24 * 30,
            'y': 60 * 60 * 24 * 365,
        }.get(unit)

    def query_time(self):
        """计算query url的start和end"""
        end_timestamp = self.task_time
        time_duration = self.strategy['tsd_rule']['time_duration']
        time_unit = self.strategy['tsd_rule']['time_unit']
        seconds = self.unit_to_seconds(time_unit) * float(time_duration)
        start_timestamp = int(end_timestamp - seconds)
        return start_timestamp, end_timestamp

    @property
    def groups_keys(self):
        """告警策略的分组tag的keys"""
        tags = self.strategy.get('tsd_rule', {}).get('group', [])
        return [kv['key'] for kv in tags]

    @staticmethod
    def comp(real_val, comparison, expect_val):
        """比较符判断"""
        # TODO: safety
        # return literal_eval(f'float({real_val}) {comparison} float({expect_val})')
        return eval(f'float({real_val}) {comparison} float({expect_val})')

    def check_group_state(self, strategy, task_time, group_state):
        """检查判断每个分组的状态，如有变化，发送通知到redis消息队列"""
        r = self.redis_cli
        STRATEGY_NOTICE = False
        for group, state in group_state.items():
            ret = r.getset(f'strategy:{strategy["_id"]}:{group}:state', json.dumps(state))
            GROUP_NOTICE = False
            if ret is None:
                if state['status'] == 'ALERT':
                    GROUP_NOTICE = True
            else:
                last_group_state = json.loads(ret)
                if last_group_state['status'] != state['status']:
                    GROUP_NOTICE = True
            if GROUP_NOTICE:
                STRATEGY_NOTICE = True
                alert_type = '告警产生' if state['status'] == 'ALERT' else '告警撤销'
                channel = self.get_channel()
                message = {
                    'strategy_id': str(strategy['_id']),
                    'strategy_name': strategy['property']['name'],
                    'alert_time': task_time,
                    'alert_info': f'【{alert_type}】\nGroup: {group}\nInfo: {state["info"]}',
                    'is_recover': True if state['status'] == 'OK' else False,
                    # 'group': group
                }
                if channel == 'notice:slack':
                    slack = self.get_slack_attr()
                    message.update(**slack)
                elif channel == 'notice:mail':
                    mail = self.get_mail_attr()
                    message.update(**mail)
                r.publish(channel, json.dumps(message))
                LOG.debug(f'Message is published by channel({channel}) => {message}')
        return STRATEGY_NOTICE

    def set_strategy_status(self, strategy_id, status):
        """更新策略状态：on/alert"""
        cli = self.mongo_cli
        db = cli['argus-alert']
        db['strategy'].update({'_id': ObjectId(strategy_id)},
                              {'$set': {
                                  'status': status
                              }}
                              )
        LOG.debug(f'Strategy({strategy_id}) status is updated to {status}.')

    def get_channel(self):
        """根据告警策略，获取publish的channel"""
        notify_method = self.strategy['notify']['notify_method']
        return f'notice:{notify_method}'

    def get_slack_attr(self):
        """获取通知对象的slack配置"""
        # TODO：用户管理完善后再做
        return {
            'slack_hook': 'https://hooks.slack.com/services/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'
        }

    def get_mail_attr(self):
        """获取通知对象的mail配置"""
        # TODO
        return {
            'mail_addr': 'tangyingkang@useease.com'
        }

    def get_wechat_attr(self):
        """"""
        return {}

    def notify_message(self, comparison, threshold, real_value):
        return f'告警条件: {comparison} {threshold}, 检查值: {real_value}'

    @abstractmethod
    def run(self):
        raise NotImplementedError
    #
    # async def fetch(self, session, url):
    #     with async_timeout.timeout(5):
    #         async with session.get(url) as response:
    #             return await response.json()
    #
    # async def aioget(self, url):
    #     async with aiohttp.ClientSession() as session:
    #         return await self.fetch(session, url)
