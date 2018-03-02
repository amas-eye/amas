#!/usr/bin/env python
# coding=utf8
"""
采集cpu时间片的相对值、cpu使用率

某一时刻/proc/stat的cpu数值如下：
    long@long-Ubuntu:~$ cat /proc/stat
    cpu  426215 701 115732 2023866 27329 4 557 0 0 0
    cpu0 218177 117 57458 1013633 8620 0 6 0 0 0
    cpu1 208038 584 58274 1010233 18709 4 550 0 0 0
    intr 21217894 119 18974 0 0 0 0 0 1 1 0 0 0 0 0 0 0 0 146350 0 647836 370 86696 3 146156 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    ctxt 38682044
    btime 1362301653
    processes 10118
    procs_running 1
    procs_blocked 0
    softirq 11177991 0 6708342 2178 148765 86792 0 14537 1507468 29072 2680837

http://man7.org/linux/man-pages/man5/proc.5.html
cpu行的参数意思解释(从左到右)：
user (426215)   Time spent in user mode.
nice (701)      Time spent in user mode with low priority(nice).
system (115732) Time spent in system mode.
idle (2023866)  Time spent in the idle task.  This value should be USER_HZ times the second entry in the /proc/uptime pseudo-file.
iowait (27329)  Time waiting for I/O to complete.
irq (4)         Time servicing interrupts.
softirq (557)   Time servicing soft interrupts.
steal （0）      Stolen time, which is the time spent in other operating systems when running in a virtualized environment
guest （0）      Time spent running a virtual CPU for guest operating systems under the control of the Linux kernel.
guest_nice （0） Time spent running a niced guest (virtual CPU for guest operating systems under the control of the Linux kernel).

CPU总时间(jiffies)=user+system+nice+idle+iowait+irq+softirq+steal+guest+guest_nice

计算CPU使用率的方法：
    两个采集点的时间间隔 = t2 - t1
    cpu usage=(1 - (t2的空闲时间片 - t1的空闲时间片)/(t2的总时间片 - t1的总时间片)) * 100%
"""
import sys
import multiprocessing

from argus_collector.collectors.common import *
from argus_collector.collectors.etc.cpu_jiffies_conf import *

DATA_PATH = os.path.join(DATA_DIR, 'cpu_jiffies.data')
TIME_INTERVAL = os.path.basename(os.path.dirname((os.path.abspath(__file__)))).strip()
FIELDS = ['user', 'nice', 'system', 'idle', 'iowait', 'irq', 'softirq', 'steal', 'guest', 'guest_nice']


def get_cpu_jiffies():
    """
    :return: cpu jiffies的列表, FIELDS字段值
    """
    with open('/proc/stat') as f_proc_stat:
        cpu_jiffies = f_proc_stat.readline()
    if not str(cpu_jiffies).startswith('cpu'):
        raise Exception('Could not read cpu jiffies! line1 from /proc/stat: ' + str(cpu_jiffies))
    return map(int, cpu_jiffies.strip().split()[1:])


def get_total_jiffies(cpu_jiffies):
    return sum(cpu_jiffies)


def get_idle_jiffies(cpu_jiffies):
    return cpu_jiffies[3]


def main():
    current_time = int(time.time())
    if TIMESTAMP_ALIGN:
        send_time = current_time - current_time % int(TIME_INTERVAL)
    else:
        send_time = current_time

    # 获取cpu数据
    values_now = get_cpu_jiffies()

    # 获取上次采集的cpu数据，如果有数据，才计算cpu使用率并输出
    last_data = get_last_data(DATA_PATH)
    if last_data is not None:
        last_timestamp = last_data.keys()[0]
        values_last = last_data[last_timestamp]

        # 计算CPU使用率
        total_last = get_total_jiffies(values_last)
        idle_last = get_idle_jiffies(values_last)
        total_now = get_total_jiffies(values_now)
        idle_now = get_idle_jiffies(values_now)
        cpu_usage = format(1 - (float(idle_now - idle_last) / float(total_now - total_last)), '0.2f')

        print('cluster.cpu.usage {0} {1}'.format(send_time, cpu_usage))

        sys.stdout.flush()

    # 不管怎样最后都要保存更新这次的cpu数据
    save_data(DATA_PATH, values_now, current_time)
    # to collector cpu cores
    print('cluster.cpu.cores {0} {1}'.format(send_time, multiprocessing.cpu_count()))


if __name__ == '__main__':
    main()
