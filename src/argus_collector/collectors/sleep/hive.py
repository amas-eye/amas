#!/usr/bin/python
# coding=utf-8
"""
//TODO 增加metastore对后端数据库连接的检查
"""
import os
import re
import sys
import socket
import urllib2
import time

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from argus_collector.collectors.etc.hive_config import *


def main():
    def split_pid(line):
        line_split = line.split(" ")
        pid = line_split[0]
        return pid

    def get_pidstat_line(cmd):
        content_all = os.popen(cmd).read()
        content = content_all.split("\n")
        data = re.split("\s+", content[3])
        return data

    def get_pidstat(pid):
        cmd = ['pidstat -u -p {pid}'.format(pid=pid),
               'pidstat -r -p {pid}'.format(pid=pid),
               'pidstat -d -p {pid}'.format(pid=pid),
               ]
        returndict = {}
        for item in cmd:
            if re.findall("-u", item):
                data = get_pidstat_line(item)
                returndict['cpu_user_rate'] = data[3]
                returndict['cpu_system_rate'] = data[4]
            elif re.findall("-r", item):
                data = get_pidstat_line(item)
                returndict['mem_rss'] = data[6]
                returndict['mem_virtual'] = data[5]
            else:
                data = get_pidstat_line(item)
                returndict['read_speed'] = data[3]
                returndict['write_speed'] = data[4]
        return returndict

    def get_charter(hiveconf):
        tree = ET.parse(hiveconf)
        root = tree.getroot()
        title = root.findall('property')
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        for item in title:
            name = item.find('name').text
            value = item.find('value').text
            if name == "hive.metastore.uris":
                config_ip = value.split(":")[1].split("//")[1]
                if config_ip == "127.0.0.1" or config_ip == ip:
                    try:
                        response = urllib2.urlopen('http://127.0.0.1:10002')
                        return "both"
                    except urllib2.URLError:
                        return "metastore"
                else:
                    return "hive_server"

    def get_metastore_num(hiveconf):
        tree = ET.parse(hiveconf)
        root = tree.getroot()
        title = root.findall('property')
        metastore_num = 0
        for item in title:
            name = item.find('name').text
            value = item.find('value').text
            if name == "hive.metastore.uris":
                metastore_num += 1
        return metastore_num

    def get_alive_metastore(hivepid, metastore_uri_list):
        """
        稍后还需要补全如果没有lsof命令的情况
        :param hivepid:
        :param metastore_uri_list:
        :return:
        """
        count = 0
        try:
            content = os.popen('lsof -i | grep {pid}'.format(pid=hivepid)).read()
            content = content.split("\n")
            state = "ESTABLISHED"
            for item in content:
                for uri in metastore_uri_list:
                    if not re.findall(uri, item) and re.findall(state, item):
                        count += 1
            return count
        except TypeError:
            pass

    def printdata(result_dict, ts, tags):
        for item in result_dict.keys():
            print "hadoop.hive.{metric} {ts} {value} {tags}".format(
                metric=item, ts=ts, value=result_dict[item], tags=tags
            )

    def get_metastore_uri(hiveconf):
        tree = ET.parse(hiveconf)
        root = tree.getroot()
        title = root.findall('property')
        uri_list = []
        for item in title:
            name = item.find('name').text
            value = item.find('value').text
            if name == "hive.metastore.uris":
                value = value.split("//")
                uri = value[1]
                uri_list.append(uri)
        return uri_list

    def get_metastore_link_count(metapid):
        count = 0
        try:
            content = os.popen('lsof -i | grep {pid}'.format(pid=metapid)).read()
            content = content.split("\n")
            state = "ESTABLISHED"
            for item in content:
                if not (re.findall("mysql", item) or re.findall("3306", item)) and \
                        re.findall(state, item):
                    count += 1
            return count
        except TypeError:
            pass

    datapath = "{basedir}/{data}".format(basedir=os.path.dirname(
        os.path.dirname((os.path.abspath(__file__)))), data="data")

    pidfilepath = "{datadir}/{filename}".format(
        datadir=datapath, filename="pidfile")

    if os.path.exists(pidfilepath):
        metapid = 0
        hive_server_pid = 0
        with open(pidfilepath, 'r') as f:
            for item in f:
                item = item.split(":")
                if item[0] == "metapid":
                    metapid = item[1]
                elif item[0] == "hive_server_pid":
                    hive_server_pid = item[1]
    else:
        metapid_line = os.popen('jps -v | grep "hive" | grep "meta" ').read()
        hive_server_pid_line = os.popen('jps -v | grep "hive" | grep -v "meta"').read()
        metapid = split_pid(metapid_line)
        hive_server_pid = split_pid(hive_server_pid_line)
        pid_dict = {"metapid": metapid, "hive_server_pid": hive_server_pid}
        with open(pidfilepath, 'w') as f:
            for item, key in pid_dict.items():
                if item:
                    f.write("{pidname}:{pid}\n".format(pidname=item, pid=key))
    if maunal_charater == None:
        charater = get_charter(hive_config_path)
    else:
        charater = maunal_charater
    uri_list = get_metastore_uri(hive_config_path)
    ts = int(time.time())
    if charater == "metastore":
        result = get_pidstat(metapid)
        tags = "node=metastore"
        result['metastore_link_count'] = get_metastore_link_count(metapid)
        printdata(result, ts, tags)
    elif charater == "hive_server":
        result = get_pidstat(hive_server_pid)
        total_metastore_num = get_metastore_num(hive_config_path)
        alive_metastore_num = get_alive_metastore(hive_server_pid, uri_list)
        result['metastore_num'] = total_metastore_num
        result['alive_metastore_num'] = alive_metastore_num
        result['dead_metastore_num'] = int(total_metastore_num) - \
                                       int(alive_metastore_num)
        tags = "node=hive_server"
        printdata(result, ts, tags)
    else:
        result_meta = get_pidstat(metapid)
        result_hive = get_pidstat(hive_server_pid)
        total_metastore_num = get_metastore_num(hive_config_path)
        alive_metastore_num = get_alive_metastore(hive_server_pid, uri_list)
        result_meta['metastore_link_count'] = get_metastore_link_count(metapid)
        result_hive['metastore_num'] = total_metastore_num
        result_hive['alive_metastore_num'] = alive_metastore_num
        result_hive['dead_metastore_num'] = int(total_metastore_num) - \
                                            int(alive_metastore_num)
        result = dict(result_meta, **result_hive)
        tags = "node0=hive_server node1=metastore"
        printdata(result, ts, tags)


if __name__ == "__main__":
    sys.exit(main())
