# coding=utf-8
"""url hander的实现
"""
import tornado.web
from redis import Redis

from argus_alert.core.rest.status_code import *
from argus_alert.core.rest.connection_manager import REDIS_POOL


class BaseHandler(tornado.web.RequestHandler):
    """BaseHandler"""
    SUPPORTED_METHODS = ("HEAD", "GET", "POST", "DELETE", "PUT")

    def prepare(self):
        pass    # hook

    @property
    def rdb(self):
        return Redis(connection_pool=REDIS_POOL, decode_responses=True)

    def response(self, code, data=None, msg=None):
        ret = {'code': code}
        if data:
            ret['data'] = data
        if msg:
            ret['msg'] = msg
        self.write(ret)


class MainHandler(BaseHandler):
    """/api/alert
    """
    def head(self, *args, **kwargs):
        """"""

    def get(self, *args, **kwargs):
        self.response(CODE_OK, 'Argus-alert RESTful API')


class VersionHandler(BaseHandler):
    """/api/alert/version

    获取API版本信息
    """
    def get(self, *args, **kwargs):
        self.response(CODE_OK, '1.0')


class DocumentHandler(BaseHandler):
    """/api/alert/doc

    获取API接口注释文档
    """
    def get(self, *args, **kwargs):
        items = ["{0}\n".format(cls.__doc__).replace('\n', '<br>') for cls in BaseHandler.__subclasses__()]
        self.render('ApiDoc.html', items=items)


class StrategyHandler(BaseHandler):
    """/api/alert/strategy

    返回告警策略的信息
    """

    def get(self, strategy_id=None, *args, **kwargs):
        r = self.rdb
        if strategy_id is None:
            strategy_ids = r.lrange('strategy', 0, -1)
            data = [[_id, r.hgetall('strategy:{}'.format(_id))] for _id in strategy_ids]
        else:
            data = r.hgetall('strategy:{}'.format(strategy_id))

        self.response(CODE_OK, data)


class StateHandler(BaseHandler):
    """/api/alert/state

    返回告警策略的状态
    """
    def get(self, strategy_id=None, *args, **kwargs):
        r = self.rdb
        if strategy_id is None:
            strategy_ids = r.lrange('strategy', 0, -1)
            data = {}
            for _id in strategy_ids:
                states = r.zrevrange('strategy:{}:state'.format(_id), 0, 0)
                if states:
                    data[_id] = states[0]
                else:
                    data[_id] = None
        else:
            states = r.zrevrange('strategy:{}:state'.format(strategy_id), 0, 0)
            if states:
                data = states[0]
            else:
                data = None

        self.response(CODE_OK, data)


class CommandHandler(BaseHandler):
    """/api/alert/command

    触发内部操作的指令，如重载告警策略等
    """
    def get(self, *args, **kwargs):
        try:
            if self.request.arguments.get('reload_strategy', b'false')[0] == b'true':
                print('Got cmd: reload_strategy.')
                self.reload_strategy()
        except Exception as e:
            pass
            self.response(CODE_FAIL, msg=str(e))
        else:
            self.response(CODE_OK)

    def reload_strategy(self):
        r = self.rdb
        r.publish(CHANNEL_CMD_RELOAD_STRATEGY, CMD_RELOAD_STRATEGY)
        print('cmd:reload_strategy is published.')


class MonitorHandler(BaseHandler):
    """/api/alert/monitor

    返回用于监控统计的性能数据
    """
    def get(self, *args, **kwargs):
        """"""


class AlertHandler(BaseHandler):
    """/api/alert/history

    返回告警通知记录
    """
    def get(self, *args, **kwargs):
        return


if __name__ == '__main__':
    pass