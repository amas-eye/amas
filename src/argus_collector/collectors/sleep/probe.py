#!/usr/bin/python
# coding=utf8
"""
这个脚本是用于在probe提取数据来进行java web应用的性能并发情况
"""
import json
import os
import sys
import time

import requests
from requests.auth import HTTPBasicAuth

from argus_collector.collectors.etc.probe_conf import *


def login(url, username, password, session):
    """
    用于尝试登陆，保证配置中用户名和密码是正确的
    :param url:
    :param username:
    :param password:
    :param session:
    :return:
    """
    response = session.get(url=url, auth=HTTPBasicAuth(username, password))
    if response.status_code == 200:
        print "login_success"
    elif response.status_code == 401:
        print "please check your username and password"


def ensure_has_list(data_structure):
    """
    用于保证把空的内容剔除出去
    :param data_structure:
    :return:
    """
    # for item in range(len(data_structure)):
    #     if not data_structure[item]:
    #         data_structure.__delitem__(item)

    # return data_structure

    return [_ for _ in data_structure if _]


def printdata(name, value, app, tag):
    """
    :param name:
    :param value:
    :param app:
    :param tag:
    :output
    print appname.metric ts value appname=appname tag
    example:
    probe(2).Avg_response_time 1502781985 1 appname=probe(2) plat=tomcat_java
    """
    ts = int(time.time())
    tag_split = tag.replace("||", " ")
    print "{a}.{n} {t} {v} appname={app} {tag}".format(
        a=app,
        n=name,
        t=ts,
        v=value,
        app=app,
        tag=tag_split
    )


def parse_html(useable_session, url, appname, tag):
    """
    这个函数是利用session对象来进行发送，
    :param useable_session:
    :param url:
    :param appname: 为发送到tsdb中的metricname的一部分，是你监控应用的名字
    :param tag: type==str
    :return:
    """
    response = useable_session.get(url=url,
                                   auth=HTTPBasicAuth("probe123", "123456")
                                   )
    data = response.content
    data = data.rstrip().lstrip()
    data = data.split('<span class="name">')
    for item in data:
        item = item.rstrip()
        item = item.replace("</span>&nbsp;", "")
        item = item.replace("&nbsp", "").rstrip()
        split_item = item.split(":")
        split_item = ensure_has_list(split_item)
        try:
            if split_item:
                name = split_item[0]
                value = split_item[1]
                name = name.replace(" ", "_")
                value = value.replace(";", "")
                value = value.rstrip()
                printdata(name, value, appname, tag)
        except IndexError:
            print "IndexError"


def main():
    probe_url = "http://{ip}:{port}/{app}".format(
        ip=PROBE_IP,
        port=PROBE_PORT,
        app=PROBE_APP
    )
    app_split = MONITORING_APP_NAME.split("||")
    app_split = ensure_has_list(app_split)
    for item in app_split:
        req_url = "{url}/appreqdetails.ajax?webapp=%2f{e}".format(
            url=probe_url,
            e=item
        )
        response_time_url = "{url}/appprocdetails.ajax?webapp=%2f{e}".format(
            url=probe_url,
            e=item
        )
        session = requests.Session()
        login(probe_url, PROBE_USERNAME, PROBE_PASSWORD, session)
        parse_html(session, req_url, item, PROBE_TAG)
        parse_html(session, response_time_url, item, PROBE_TAG)


if __name__ == "__main__":
    sys.exit(main())
