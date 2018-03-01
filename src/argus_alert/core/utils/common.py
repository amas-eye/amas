# coding=utf-8
"""
"""
import functools
import json
import types
import sys
import os
import signal
import atexit

from argus_alert.etc.bootstrap import BASE_DIR


def cache(func):
    """缓存装饰器，如果函数或类的名和参数相同，返回之前保存的结果"""
    _cached = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 检查是否_instances的key；如果是，直接返回之前的结果
        key = '<{0}_{1}_{2}>'.format(func.__name__, args, kwargs)
        if key not in _cached:
            _cached[key] = func(*args, **kwargs)
        return _cached[key]

    return wrapper


def decode(encoded, encoding):
    if isinstance(encoded, bytes):
        return encoded.decode(encoding)
    if isinstance(encoded, dict):
        return {k.decode(encoding): v.decode(encoding) for k, v in encoded.items()}
    if isinstance(encoded, list):
        return [ele.decode(encoding) for ele in encoded]


decode_utf8 = functools.partial(decode, encoding='utf-8')


def daemonize(pid_file=None):
    """
    创建守护进程
    :param pid_file: 保存进程id的文件
    :return:
    """
    pid = os.fork()
    if pid:
        sys.exit(0)

    os.chdir('/')
    os.umask(0)
    os.setsid()

    _pid = os.fork()
    if _pid:
        sys.exit(0)

    sys.stdout.flush()
    sys.stderr.flush()

    with open('/dev/null') as read_null, open('/dev/null', 'w') as write_null:
        os.dup2(read_null.fileno(), sys.stdin.fileno())
        os.dup2(write_null.fileno(), sys.stdout.fileno())
        os.dup2(write_null.fileno(), sys.stderr.fileno())

    if pid_file:
        with open(pid_file, 'w+') as f:
            f.write(str(os.getpid()))
        atexit.register(os.remove, pid_file)


def save_pid(pid, pid_name=''):
    """保存pid"""
    pid = str(pid).strip()
    if not pid_name:
        pid_name = pid
    pidfile = os.path.join(BASE_DIR, 'tmp', f'{pid_name}.pid')
    with open(pidfile, 'w') as f:
        f.write(pid)
    return pidfile


def kill_pid(pidfile, remove_file=True):
    with open(pidfile) as f:
        pid = str(f.read()).strip()
    try:
        os.kill(int(pid), signal.SIGKILL)
    except:
        pass
    os.remove(pidfile)


def kill_all():
    """杀死tmp/目录下的所有pid"""
    for f in os.listdir(os.path.join(BASE_DIR, 'tmp')):
        if f.endswith('.pid'):
            pidfile = os.path.join(BASE_DIR, 'tmp', f)
            kill_pid(pidfile)


if __name__ == '__main__':
    pass

    kill_all()