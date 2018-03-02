#!/usr/bin/env python3
# coding=utf-8
"""统一管理脚本
"""
from multiprocessing import Process

from argus_alert.core.inspect.manager import DriverManager, ExecutorManager
from argus_alert.core.utils.entrypoint import load_config
from argus_alert.core.utils.log import timed_logger
from argus_alert.core.notice.handler import run_notice_handler
from argus_alert.core.utils.common import save_pid

LOG = timed_logger()

HELP_MSG = """
help message...
"""


def main():
    """"""
    config = load_config()
    LOG.info(f'config loaded: {config}')

    ps = []

    # 启动driver进程
    if config.get('START_DRIVER', False):
        driver_manager = DriverManager(
            host=config['DRIVER_HOST'], port=config['DRIVER_PORT'], authkey=config['AUTH_KEY'],
            redis_addr=config['REDIS_ADDR'],
            mongo_addr=config['MONGO_ADDR']
        )
        driver_ps = Process(target=driver_manager.start, name='DriverProcess')
        driver_ps.start()
        ps.append(driver_ps)
        LOG.info('Driver process started.')
        save_pid(driver_ps.pid, driver_ps.name)

    # 启动executor进程
    if config.get('START_EXECUTOR', False):
        executor_workers_num = int(config['EXECUTOR_WORKER'])
        executor_ps = [ExecutorManager(
            host=config['DRIVER_HOST'], port=config['DRIVER_PORT'], authkey=config['AUTH_KEY'],
            redis_addr=config['REDIS_ADDR'],
            mongo_addr=config['MONGO_ADDR'],
            tsd_addr=config['OPENTSDB_ADDR'],
            name=f'ExecutorProcess-{n}'
        ) for n in range(executor_workers_num)]
        for p in executor_ps:
            p.start()
            save_pid(p.pid, p.name)
        ps.extend(executor_ps)
        LOG.info(f'Executor process started, {executor_workers_num} workers.')

    # 启动通知处理进程
    if config.get('START_NOTIFIER', False):
        notifier_workers_num = int(config['NOTIFIER_WORKER'])
        notifier_ps = [Process(target=run_notice_handler, name=f'NotifierProcess-{n}', kwargs=dict(
            mongo_addr=config['MONGO_ADDR'],
            redis_addr=config['REDIS_ADDR'],
            topics=['notice:*'],
        )) for n in range(notifier_workers_num)]
        for p in notifier_ps:
            p.start()
            save_pid(p.pid, p.name)
        ps.extend(notifier_ps)
        LOG.info(f'Notifier process started, {notifier_workers_num} workers')

    # for p in ps:
    #     p.join()


if __name__ == '__main__':
    pass
    main()

