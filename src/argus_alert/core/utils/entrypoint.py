# coding=utf-8
"""配置管理
"""
import json
import sys
from optparse import OptionParser

from redis import Redis

from argus_alert.etc.bootstrap import *
from argus_alert.core.utils.common import decode_utf8


class ArgParser(object):
    """命令行参数解析

    >>> ArgParser().args_dict
    {}
    >>> ArgParser(['config_handler.py', '--start-driver', '--driver-port', 7001, '--authkey', 'argus@ue']).args_dict
    {'START_DRIVER': True, 'DRIVER_PORT': 7001, 'AUTH_KEY': 'argus@ue'}

    """
    def __init__(self, cmd_args=None):
        """
        :param cmd_args: 命令行参数，默认 sys.argv
        :type cmd_args: list
        """
        self._cmd_args = sys.argv if cmd_args is None else cmd_args
        self._options, _ = self.parse_args(self._cmd_args)
        self._args_dict = extract_upper_vars(self._options, ignore_none_value=True)

    @property
    def args_dict(self):
        return self._args_dict

    def parse_args(self, sys_args):
        parser = OptionParser(usage='python %prog [--dev|--test|--prod|'
                                    '--tsd|--api-serve|--redis|--mongo|'
                                    '--start-driver|start-executor|--driver-host|--driver-port|--authkey]',
                              description='Argus-alert.')
        parser.add_option('--dev', dest='ENV_DEV', action='store_true',
                          help='use development environ configuration')
        parser.add_option('--test', dest='ENV_TEST', action='store_true',
                          help='use test environ configuration')
        parser.add_option('--prod', dest='ENV_PROD', action='store_true',
                          help='use production environ configuration')
        parser.add_option('--tsd', dest='OPENTSDB_ADDR',
                          help='opentsdb address, should be like "<ip>:<port>"')
        parser.add_option('--api-serve', dest='API_SERVE_ADDR',
                          help='restful api server addr, should be like "<ip>:<port>"')
        parser.add_option('--redis', dest='REDIS_ADDR',
                          help='redis address, should be like "redis:///@<ip>:<port>/<db>"')
        # parser.add_option('--use-mongo-conf', dest='USE_MONGO_CONF', default=False,
        #                   help='use config from mongodb')
        parser.add_option('--mongo', dest='MONGO_ADDR',
                          help='mongo address, should be like "mongodb://<ip>:<port>"')
        parser.add_option('--start-driver', dest='START_DRIVER', action='store_true',
                          help='bootstrap driver process')
        parser.add_option('--start-executor', dest='START_EXECUTOR', action='store_true',
                          help='bootstrap executor process')
        parser.add_option('--executor-worker', dest='EXECUTOR_WORKER',
                          help='set worker numbers for executor')
        parser.add_option('--driver-host', dest='DRIVER_HOST',
                          help='set host for driver process')
        parser.add_option('--driver-port', dest='DRIVER_PORT',
                          help='set port for driver process')
        parser.add_option('--authkey', dest='AUTH_KEY',
                          help='set auth string for multiprocessing.Process')
        parser.add_option('--start-notifier', dest='START_NOTIFIER', action='store_true',
                          help='bootstrap notifier process')
        parser.add_option('--notifier-worker', dest='NOTIFIER_WORKER',
                          help='set worker numbers for notifier')
        options, args = parser.parse_args(sys_args)
        return options, args


def extract_upper_vars(obj, ignore_none_value=False):
    """获取对象或实例的大写变量

    :param obj: 类
    :param ignore_none_value: 是否忽略值为None的变量

    >>> class Foo(object): BAR = 'BAR'; bar = 'bar'; NONE = None
    >>> extract_upper_vars(Foo)
    {'BAR': 'BAR', 'NONE': None}
    >>> extract_upper_vars(Foo, ignore_none_value=True)
    {'BAR': 'BAR'}
    """
    if ignore_none_value:
        return {k: v for k, v in obj.__dict__.items() if k.isupper() and v is not None}
    else:
        return {k: v for k, v in obj.__dict__.items() if k.isupper()}


def load_config():
    """载入启动配置

    配置的加载步骤（默认-命令行参数-场景-数据库）：
    1）加载默认配置项DefaultConfig
    2）
        2.1）用命令行参数配置覆盖之
        2.2）如果有指定环境（开发/测试/生产），用指定环境下的配置覆盖上述默认配置
    3) 加载运行配置RunningConfig

    >>> load_config()
    {'OPENTSDB_ADDR': 'localhost:4242', 'REDIS_ADDR': 'redis:///@localhost:6379/0', 'MONGO_ADDR': 'mongodb://localhost:27017/', 'API_SERVE_ADDR': '0.0.0.0:8888', 'DRIVER_HOST': 'localhost', 'DRIVER_PORT': 7001, 'AUTH_KEY': 'argus@useease', 'LOG_LEVEL': 'DEBUG', 'LOG_DIR': '/Users/eacon/useease/project_code/argus/argus-alert/argus_alert/logs', 'EXECUTOR_WORKER': 2, 'EXECUTOR_COROUTINES': 2, 'EXECUTOR_THREADS': 2}
    """
    config_dict = extract_upper_vars(DefaultConfig)
    cmd_args = ArgParser().args_dict
    config_dict.update(cmd_args)

    if config_dict.get('ENV_PROD', False):
        prod_config = extract_upper_vars(ProdConfig)
        config_dict.update(prod_config)
    elif config_dict.get('ENV_TEST', False):
        test_config = extract_upper_vars(TestConfig)
        config_dict.update(test_config)
    elif config_dict.get('ENV_DEV', False):
        dev_config = extract_upper_vars(DevConfig)
        config_dict.update(dev_config)

    config_dict.update(extract_upper_vars(RunningConfig))
    return config_dict


if __name__ == '__main__':
    pass


    test_args = ['/Users/eacon/useease/project_code/argus/argus-alert/argus_alert/core/utils/config_handler.py']
    test_args.extend(['-d', '--log-level', 'debug', '--log-dir', '/tmp'])
    test_args.extend(['--redis', 'redis:///@localhost:6379/0', '--redis-conf', 'config:dev'])

    print(load_config())
