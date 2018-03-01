# coding=utf-8
"""基于tornado的restful api服务进程
"""
import tornado.web
import tornado.ioloop
from redis import ConnectionPool

from argus_alert.core.rest.handler import *
from argus_alert.core.rest.connection_manager import REDIS_POOL


def main(redis_addr='redis:///@localhost:6379/0'):
    """"""
    # redis连接池
    global REDIS_POOL
    REDIS_POOL = ConnectionPool.from_url(redis_addr)

    # tornado app
    app = tornado.web.Application([
        (r'/api/alert', MainHandler),
        (r'/api/alert/version', VersionHandler),
        (r'/api/alert/doc', DocumentHandler),

        (r'/api/alert/strategy', StrategyHandler),
        (r'/api/alert/strategy/(.+)', StrategyHandler),

        (r'/api/alert/state', StateHandler),
        (r'/api/alert/state/(.+)', StateHandler),

        (r'/api/alert/command', CommandHandler),

        (r'/api/alert/monitor', MonitorHandler),

    ],
        debug=True,
        autoreload=True
    )
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()