#!/usr/bin/env python
# coding=utf-8
"""采集管理的api

1）管理采集指标，查询tsd已收集的指标信息
2）agent如果配置了管理器地址，可以向管理器定时发送自身信息，管理器统一展示各个agent的分布情况、采集状态 """
import fcntl
import json
import os
import sys
import signal
import time
import threading
from optparse import OptionParser
from multiprocessing import Process

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from argus_collector.conf.settings import *
from argus_collector.web.bottle import Bottle, run, request, template, abort, response
from argus_collector.web.status_code import *
from argus_collector.web.data.settings import *
from argus_collector.web.utils import get_logger, get_tags
import argus_collector.web.tsdb_metric as tsdb_metric
import argus_collector.web.db as db
import argus_collector.web.status_code as status_code

api_logger = get_logger(API_LOG)

def serve_app():
    """"""
    app = Bottle()

    @app.get('/api/collector')
    def homepage():
        """主页"""
        return template('homepage.tpl', {})

    @app.get('/api/stats')
    def stats():
        """返回最新的状态码"""
        codes = {}
        for i in dir(status_code):
            if i.isupper():
                codes[i] = eval(i)
        return codes

    @app.get('/api/collector/metric')
    def get_metric():
        """
        所有细节封装在db模块下，api服务器只需根据result['code']记录日志
        """

        search = request.GET.get('search', '')
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))

        result = None
        if search:  # return related metrics in db
            result = db.get_records_via_kw(search, offset, limit)
            api_logger.info('Query key word <{0}> limit <{1}> offset <{2}>'.format(search, limit, offset))
        else:
            result = db.get_records(offset, limit)
            api_logger.info('Query all records limit <{0}> offset <{1}>'.format(limit, offset))

        if result['code'] == DB_ERROR:
                api_logger.warn('DB ERROR')

        return result

    @app.post('/api/collector/metric')
    def post_metric():
        new_record = request.json
        result = db.update(new_record)
        if result['code'] == UPDATE_FAILED:
            api_logger.warn('Refused a post request')
        elif result['code'] == UPDATE_UNCOMPLETED:
            api_logger.warn('Refused {0}, Updated {1}'.format(
                len(new_record) - result['updated'] - result['unknown'], result['updated']))
        elif result['code'] == UPDATE_ACCEPTED:
            api_logger.warn('Accepted {0}'.format(result['updated']))
        elif result['code'] == DB_ERROR:
            api_logger.warn('DB error')
        return result

    @app.get('/api/collector/agent/<host>')
    @app.get('/api/collector/agent')
    def get_agent(host=''):
        agent_info = load_agent(host)
        if agent_info is None:
            return abort(404)
        return {
            'code': CODE_OK,
            'data': agent_info
        }

    @app.post('/api/collector/agent')
    def post_agent():
        """采集器向管理者提交自身信息

        POST json数据，字段至少包含：
            host: 自身的host地址
            tsd_host: 发往哪个tsd数据库host
            tsd_port: 发往哪个tsd数据库port
            collectors: 正在运行的采集器
            uptime: 采集器进程uptime（秒）
        """
        try:
            agent_info = request.json
            agent_info['heartbeat_time'] = int(time.time())
            dump_agent(agent_info)
            api_logger.info(agent_info['host'] + 'pushed status.')
        except Exception as e:
            return {'code': CODE_FAIL, 'msg': str(e)}
        else:
            return {'code': CODE_OK}

    @app.get('/api/tsdb')
    def tsdb_helper():
        period = request.GET.get('period')
        metric = request.GET.get('metric')
        result = get_tags(period, metric)
        return {
                'data': result
        }
     


    def dump_agent(agent_info):
        """将采集器信息持久化到文件
        """
        dumpfile = os.path.join(BASE_DIR, 'web', 'agents', '{0}.json'.format(agent_info.get('host', '_')))
        df = open(dumpfile, 'w')
        fcntl.flock(df.fileno(), fcntl.LOCK_EX)
        df.write(json.dumps(agent_info, indent=2))
        df.flush()
        df.close()

    def load_agent(host=''):
        """从文件中载入采集器信息"""
        if host:
            dumfile = os.path.join(BASE_DIR, 'web', 'agents', '{0}.json'.format(host))
            if not os.path.exists(dumfile):
                return None
            df = open(dumfile)
            fcntl.flock(df.fileno(), fcntl.LOCK_EX)
            return json.load(df)
        else:
            agent_dir = os.path.join(BASE_DIR, 'web', 'agents')
            agent_list = [f for f in os.listdir(agent_dir) if f.endswith('.json')]
            agents = []
            if agent_list:
                for agent in agent_list:
                    agent_host = str(agent).rstrip('.json')
                    agent_info = load_agent(agent_host)
                    agents.append(agent_info)
            return agents

    return app


def update_process(count, interval):
    """
    The entrance of local db updating process.
    """

    update_logger = get_logger(UPDATE_LOG)
    while True:
        update_logger.info('update process run on <{0}> using <{1}> threads every <{2}> seconds>'.format(
            os.getpid(), count, interval))
        start_time = time.time()
        data_set = tsdb_metric.get_metrics()  # all metrics in remote OPENTSDB
        container = []
        all_metrics = db.get_all_metrics()  # all metrics in local sqlite3 db
        update_logger.info('found <{0}> record(s) in local db'.format(len(all_metrics)))
        basic = len(data_set) / count + 1

        t_list =[]
        network_start = time.time()
        for i in range(count):
            start = i * basic 
            end = start + basic
            data = data_set[start:end]
            t = threading.Thread(target=tsdb_metric.get_last_data_points, args=(data, container))
            t_list.append(t)
        for t in t_list:
            t.start()
        for t in t_list:
            t.join()
        update_logger.info('found <{0}> metrics from remote tsdb'.format(len(container)))
        update_logger.info('network used:{0}'.format(time.time() - network_start))
        judge_time = time.time()
        # existed = new = []
        new = []
        existed = []
        if not all_metrics:
            new = [(m, t) for (m, t) in container]
        else:
            for (m, t) in container:
                if m in all_metrics:
                    existed.append((m, t))
                else:
                    new.append((m, t))
        update_logger.info('judge used:{0}'.format(time.time() - judge_time))
        update_logger.info('new record(s):<{0}>'.format(len(new)))
        update_logger.info('existed record(s):<{0}>'.format(len(existed)))

        if new:
            insert_time = time.time()
            db.insert_many(new)
            update_logger.info('insert <{0}> new record(s) used:{1}'.format(len(new), time.time() - insert_time))
        if existed:
            update_time = time.time()
            db.update_many(existed)
            update_logger.info('update <{0}> record(s) used:{1}'.format(len(existed), time.time() - update_time))
        update_logger.info('Update process used: {0}'.format(time.time() - start_time))
        time.sleep(interval)


def main():
    try:
        options, args = cmd_handler()
        if options.start:
            update()
            start()
        if options.stop:
            kill()
        if options.restart:
            restart()
    except Exception as e:
        api_logger.error("Unexpected error {}".format(e))


def start():
    write_pid()
    run(serve_app(), host='0.0.0.0', port=8001)


def write_pid():
    f = open('./pidfile', 'w')
    try:
        f.write(str(os.getpid()))
        api_logger.warn('write pid {0}'.format(os.getpid()))
    finally:
        f.close()


def kill():
    with open('./pidfile', 'r') as f:
        pid = f.read().strip()
    try:
        os.kill(int(pid), signal.SIGTERM)
        print('Stopping server')
        os.remove('./pidfile')
        time.sleep(1)
    except OSError as e:
        api_logger.error("No such process [{}], msg {}".format(pid, e))


def restart():
    kill()
    start()


def update():
    count = DB_UPDATE_CONCURRENCY 
    interval = DB_UPDATE_INTERVAL
    p = Process(target=update_process, args=(count, interval))
    p.start()


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


if __name__ == '__main__':
    main()
