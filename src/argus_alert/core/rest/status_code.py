# coding=utf-8
"""RESTful状态码、消息
"""
CODE_OK = 0
CODE_FAIL = 1000
CODE_REDIS_UNAVAILABLE = 1001

CODE_MSG = {
    CODE_OK: 'OK',
    CODE_FAIL: 'Internal Server Error!',
    CODE_REDIS_UNAVAILABLE: 'Redis server unavailable!'
}


CMD_RELOAD_STRATEGY = 'RELOAD_STRATEGY'
CHANNEL_CMD_RELOAD_STRATEGY = 'cmd:reload_strategy'