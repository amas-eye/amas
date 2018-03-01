#!/usr/bin/env python
# coding=utf8
"""
进程监控
0, 进程不存在
1, 进程正常
"""
import commands
import sys
import os
import time
import traceback
import platform

from argus_collector.collectors.etc.process_conf import *

TIME_INTERVAL = os.path.basename(os.path.dirname((os.path.abspath(__file__)))).strip()


def main():
    """"""
    for k, v in CONFIG.iteritems():
        pids = get_pid(v)
        current_time = int(time.time())
        if TIMESTAMP_ALIGN:
            send_time = current_time - current_time % int(TIME_INTERVAL)
        else:
            send_time = current_time

        if pids is not None:
            if len(pids) == 0:
                # 进程不存在
                print "{0} {1} {2} interval={3}".format(
                    k, send_time, 0, TIME_INTERVAL
                )
                continue
            for pid in pids:
                # 进程存在，发送指标值为1
                print_str = "{0} {1} {2} pid={3} interval={4}".format(
                    k, send_time, 1, pid, TIME_INTERVAL
                )
                # 发送runTime指标
                run_time = get_runTime(pid)
                runtime_str = ''
                if run_time is not None:
                    runtime_str = '{0}.runTime {1} {2} pid={3} interval={4}'.format(
                        k, send_time, run_time, pid, TIME_INTERVAL
                    )
                # 进程state
                if platform.system() == 'Linux':
                    state = get_pid_state(pid)
                    if state is not None:
                        print_str += ' state={0}'.format(state)
                        runtime_str += ' state={0}'.format(state)
                print print_str
                print runtime_str
    sys.stdout.flush()


def get_pid(cmd, **kwargs):
    """
    执行shell指令获取pid
    返回pid列表
    """
    try:
        status, output = commands.getstatusoutput(cmd)
        if status == 0:
            if str(output).strip() == '':
                return []
            else:
                return str(output).strip().split('\n')
        else:
            print >> sys.stderr, str(output)
            raise RuntimeError('Error while getting pid, cmd: {0}, output: {1}'.format(cmd, output))
    except BaseException as e:
        print >> sys.stderr, "Error: {0}\n{1}".format(e, traceback.format_exc())
        return None


def get_runTime(pid):
    """根据pid获取进程运行时间"""
    run_time = ''
    try:
        status, output = commands.getstatusoutput("ps -eo pid,etime|grep %s|awk '{print $2}'" % str(pid))
        if status != 0:
            print >> sys.stderr, str(output)
            raise RuntimeError('Error while getting pid runtime, pid: {0}, output: {1}'.format(pid, output))
        run_time = str(output).strip()
        if not run_time:
            raise RuntimeError('Error! No runtime for pid: {0}'.format(pid))
        if '-' in run_time:
            days, times = run_time.split('-')
            days = int(days.strip())
            hours, minutes, seconds = map(int, times.split(':'))
        else:
            days = 0
            times = run_time.split(':')
            if len(times) == 3:
                hours, minutes, seconds = map(int, times)
            elif len(times) == 2:
                hours = 0
                minutes, seconds = map(int, times)
            else:
                raise RuntimeError('Error while parsing process runtime: {0}'.format(run_time))
        return seconds + minutes * 60 + hours * 60 * 60 + days * 24 * 60 * 60
    except BaseException as e:
        print >> sys.stderr, "Error: {0}\npid: {1}, runtime: {2}\n{3}".format(e, pid, run_time, traceback.format_exc())
        return None


def get_pid_state(pid, *args, **kwargs):
    """
    检查进程状态
    return {
            'R': 'running',
            'S': 'sleeping',
            'D': 'uninterruptible',
            'T': 'stopped_or_traced',
            'Z': 'zombie',
            'X': 'exit',
        }.get(pid_state.upper())
    """
    cmd = "cat /proc/%s/status|grep State|awk '{print $2}'" % str(pid)
    try:
        status, output = commands.getstatusoutput(cmd)
        if status != 0:
            print >> sys.stderr, str(output)
            raise RuntimeError('Error while testing hangDead for pid: {0}'.format(pid))
        pid_state = str(output).strip()
        return pid_state
    except BaseException as e:
        print >> sys.stderr, "Error: {0}\n{1}".format(e, traceback.format_exc())
        return None


if __name__ == '__main__':
    main()
