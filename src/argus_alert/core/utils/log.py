# coding=utf-8
"""日志记录
"""
import logging
import os
import socket
import getpass
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler

from argus_alert.etc.bootstrap import RunningConfig
from argus_alert.core.utils.common import cache

LOG_LEVEL = RunningConfig.LOG_LEVEL
LOG_DIR = RunningConfig.LOG_DIR
LOG_FORMAT = '%(asctime)-15s [%(process)d:%(threadName)s][%(filename)s][L:%(lineno)d][%(levelname)s] %(message)s'
HOSTNAME = socket.gethostname()
USER = getpass.getuser()


@cache
def _logger(name='Argus'):
    """按1G大小切割，保留7份切割日志"""
    logger = logging.getLogger(name)
    logger.setLevel({
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
    }.get(LOG_LEVEL.upper(), 'DEBUG'))
    rfh = RotatingFileHandler(
        filename=os.path.join(LOG_DIR, f'{USER}@{HOSTNAME}.log'),
        maxBytes=1024 * 1024,
        backupCount=7,
        encoding='utf-8'
    )
    rfh.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(rfh)
    return logger


@cache
def timed_logger(name='Argus'):
    """按天切割，保留30天的日志"""
    logger = logging.getLogger(name)
    logger.setLevel({
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
    }.get(LOG_LEVEL.upper(), 'DEBUG'))
    tfh = TimedRotatingFileHandler(
        filename=os.path.join(LOG_DIR, f'{USER}@{HOSTNAME}.log'),
        when='d',
        interval=1,
        backupCount=30,
        encoding='utf-8'
    )
    tfh.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(tfh)
    return logger


if __name__ == '__main__':
    LOG = timed_logger()
    LOG.info('info')
    LOG.debug('debug')
    LOG.warn('warn')
    LOG.error('error')
