# coding=utf-8
"""
"""
import time
import threading
import signal
import sys
import os
import json
import logging
from optparse import OptionParser

from argus_statistics.alert_stat import main as alert_stat_update
from argus_statistics.alert_trend import main as alert_trend_update
from argus_statistics.metric_stat import update_metric
from argus_statistics.sys_resource import update_sys_resource
# from argus_statistics.overall_health import main as overall_update
from argus_statistics.host_stat import main as host_stat_update

config = os.getcwd() + "/etc/update_config.json"

logging.basicConfig(filename="app_record.log", level=logging.DEBUG,
                    format='%(asctime)s-%(levelname)s-%(module)s:%(lineno)d-%(funcName)s: %(message)s')


def read_config(config_file):
    try:
        with open(config_file, "r") as f:
            configuration = f.readline()
            configuration = json.loads(configuration)
            interval = configuration["update_interval"]
            return int(interval)
    except FileNotFoundError:
        print("check your update_config")
        exit()


def cmd_handler():
    parser = OptionParser()
    parser.add_option('--start', dest='start', default=False, action='store_true', help='start the api server.')
    parser.add_option('--stop', dest='stop', default=False, action='store_true', help='stop the api server.')
    parser.add_option('--restart', dest='restart', default=False, action='store_true', help='restart the api server.')

    (options, args) = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        parser.exit()
    return options, args


def entrance():
    try:
        options, args = cmd_handler()
        if options.start:
            # update()
            start()
        if options.stop:
            kill()
        if options.restart:
            restart()
    except Exception as e:
        logging.error("Unexpected error {}".format(e))


def write_pid():
    f = open('./pidfile', 'w')
    try:
        f.write(str(os.getpid()))
        logging.warn('write pid {0}'.format(os.getpid()))
    finally:
        f.close()


def start():
    write_pid()
    main()


def kill():
    with open('./pidfile', 'r') as f:
        pid = f.read().strip()
    try:
        os.kill(int(pid), signal.SIGTERM)
        print('Stopping server')
        os.remove('./pidfile')
        time.sleep(1)
    except OSError as e:
        logging.error("No such process [{}], msg {}".format(pid, e))


def restart():
    kill()
    start()


def main():
    """
    这是dashboard的主入口函数
    :return:
    """
    # logging.basicConfig(filename="app_record.log", level=logging.DEBUG,
    # format = '%(asctime)s-%(levelname)s-%(module)s:%(lineno)d-%(funcName)s: %(message)s')
    logging.debug("start_dashboard.py is starting")
    time_interval = read_config(config) * 60
    print(time_interval)
    update_list = [alert_stat_update, alert_trend_update, update_metric, host_stat_update, update_sys_resource]
    while True:
        Thread_list = []
        for item in update_list:
            T = threading.Thread(target=item, args=())
            Thread_list.append(T)
        for thread in Thread_list:
            thread.start()
        logging.debug("all thread is running")
        for t in Thread_list:
            t.join()
        logging.debug("thread is all done and going to sleep")
        time.sleep(time_interval)


if __name__ == '__main__':
    # main()
    entrance()
