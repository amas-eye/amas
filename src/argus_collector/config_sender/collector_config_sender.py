# coding=utf-8

import os 
import socket
import re 
import threading
import json
import time
import sys
import logging
import urllib2 

import sys
Whole_path = os.path.dirname(os.path.dirname(os.path.abspath(os.curdir)))
# print Whole_path
sys.path.append(Whole_path)

from argus_collector.conf.settings import *
log_fmt = '%(levelname)s-%(filename)s-%(asctime)s-%(module)s:%(lineno)d-%(funcName)s: %(message)s'
logging.basicConfig(filename='config_sender.log',level=logging.DEBUG,format=log_fmt)
LOG = logging.getLogger()
## for debuger with vscode
# import ptvsd
# ptvsd.settrace('my_serect',address=('0.0.0.0',28000))

def recrusive_getpath(times):
    all_path = os.path.abspath(os.curdir)
    base_path = all_path
    for i in range(times):
        base_path = os.path.dirname(base_path)
    return base_path


def get_conf_list():
    '''
    This function is for agent to get the conf of collectors
    '''
    regex = re.compile('.*\.pyc')
    regex2 = re.compile('__init__')
    regex3 = re.compile('config.py')
    # project_path = os.path.dirname(os.path.dirname(os.path.abspath(os.curdir)))
    project_path = recrusive_getpath(1)
    conf_path = project_path +'/collectors/etc'
    all_config_list = os.listdir(conf_path)
    config_list = []
    for item in all_config_list:
        if not(re.findall(regex,item) or re.findall(regex2,item) or re.findall(regex3,item)):
            config_list.append(item)
    return conf_path,config_list


class Config_reader(threading.Thread):

    def __init__(self,lock,basemodule,config_name,result):
        super(Config_reader,self).__init__()
        # self.writefile = total_file
        self.lock = lock
        self.basemodule = basemodule
        self.config_name = config_name
        self.result = result

    def run(self):
        '''
        需要保证每个配置都目录都是以选项名 = 值为头
        并且注释(包括中文注释)前面全部需要加上#进行判断
        '''
        self.lock.acquire()
        m = __import__(self.basemodule)
        collectors = getattr(m,'collectors')
        etc = getattr(collectors,'etc')
        real_config = getattr(etc,self.config_name)
        Property = getattr(real_config,'Property')
        config_dict = {}
        for item in Property:
            name = item
            value = getattr(real_config,item)
            config_dict[name] = value
        config_dict['name'] = real_config.__name__
        write_config = json.dumps(config_dict)
        self.result.append(write_config)
        LOG.debug('{a}  config  is collected'.format(a=self.config_name))
        self.lock.release()


def main(m_ip,interval):
    ## TODO 需要把端口常开还是保持现在的使用crontab定时启动？
    # time.sleep(10)

    while True:
        c_path,c_list = get_conf_list()
        print c_list
        print c_path
        collector_path = os.path.dirname(os.path.dirname(c_path))
        print collector_path
        sys.path.append(collector_path)
        lock = threading.Lock()
        host = '192.168.0.253'  ##
        port = 8777  ## 
        base_config = 'argus_collector.collectors.etc'
        thread_list = []
        result = []
        for conf in c_list:
            conf_name = conf.split('.')[0]
            config = '{b}.{c}'.format(b=base_config,c=conf_name)
            t = Config_reader(lock,config,conf_name,result)
            thread_list.append(t)
            t.start()
        for item in thread_list:
            item.join()

        print result
        send_data = {}
        hostname = socket.gethostname()
        send_data[hostname] = result
        send_data['name'] = hostname
        send_data['timestamp'] = int(time.time())
        send_data = json.dumps(send_data)
        LOG.debug('{h} data is {d}'.format(h=hostname,d=send_data))
        print send_data
        for item in m_ip:
            ip,port = item.split(":")
            send_url = 'http://{ip}:{p}/api/collector/config_collector'.format(ip=ip,p=port)
            headers = {'Content-Type': 'application/json'}
            req = urllib2.Request(send_url,send_data,headers=headers)
            try:
                f = urllib2.urlopen(req)
                LOG.debug('config is send')
            except Exception:
                LOG.debug('send this host fail, host is {i}'.format(i=ip))
        LOG.debug('config all is send going to sleep')
        time.sleep(interval)


if __name__ == "__main__":
    num_agent = AGENT_MANAGER_TOTAL
    interval = CONFIG_SENDER_FREQUENCY
    ip_list = []
    for i in range(1,num_agent+1):
        agent = eval('AGENT_MANAGER_HOST'+str(i))
        port = eval('AGENT_MANAGER_PORT'+str(i))
        str_ip = '{a}:{b}'.format(a=str(agent),b=str(port))
        ip_list.append(str_ip)
    main(ip_list,interval)
