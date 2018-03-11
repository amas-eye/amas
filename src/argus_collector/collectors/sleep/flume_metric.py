#! /usr/bin/env python
# coding=utf8
"""
flume的度量监控数据采集

如下是一个flume的度量监控接口：
[tianxq@BDI069 ~]$ curl http://10.17.35.69:20160/metrics {"SINK.sink1":{"ConnectionCreatedCount":"2","ConnectionClosedCount":"2","Type":"SINK","BatchCompleteCount":"38","BatchEmptyCount":"48","EventDrainAttemptCount":"38480","StartTime":"1467680715075","EventDrainSuccessCount":"38480","BatchUnderflowCount":"2","StopTime":"0","ConnectionFailedCount":"0"},"SOURCE.src1":{"EventReceivedCount":"303520","AppendBatchAcceptedCount":"304","Type":"SOURCE","EventAcceptedCount":"303520","AppendReceivedCount":"0","StartTime":"1467680715454","AppendAcceptedCount":"0","OpenConnectionCount":"0","AppendBatchReceivedCount":"304","StopTime":"0"},"CHANNEL.ch1":{"ChannelCapacity":"10000","ChannelFillPercentage":"0.0","Type":"CHANNEL","ChannelSize":"0","EventTakeSuccessCount":"38480","EventTakeAttemptCount":"38531","StartTime":"1467680715071","EventPutAttemptCount":"38480","EventPutSuccessCount":"38480","StopTime":"0"}}

json格式化后如下：
{
"SINK.sink1": {
"ConnectionCreatedCount": "1",
"ConnectionClosedCount": "0",
"Type": "SINK",
"BatchCompleteCount": "19",
"BatchEmptyCount": "0",
"EventDrainAttemptCount": "19240",
"StartTime": "1467680715075",
"EventDrainSuccessCount": "19240",
"BatchUnderflowCount": "1",
"StopTime": "0",
"ConnectionFailedCount": "0"
},
"SOURCE.src1": {
"EventReceivedCount": "151760",
"AppendBatchAcceptedCount": "152",
"Type": "SOURCE",
"EventAcceptedCount": "151760",
"AppendReceivedCount": "0",
"StartTime": "1467680715454",
"AppendAcceptedCount": "0",
"OpenConnectionCount": "0",
"AppendBatchReceivedCount": "152",
"StopTime": "0"
},
"CHANNEL.ch1": {
"ChannelCapacity": "10000",
"ChannelFillPercentage": "0.0",
"Type": "CHANNEL",
"ChannelSize": "0",
"EventTakeSuccessCount": "19240",
"EventTakeAttemptCount": "19242",
"StartTime": "1467680715071",
"EventPutAttemptCount": "19240",
"EventPutSuccessCount": "19240",
"StopTime": "0",
"test": {
"haha": 100
}
}
}

需要读取SINK.sink1.EventDrainSuccessCount,SOURCE.src1.EventReceivedCount数值，并以采集当前时间为时间戳，且记录上一次时间数值，计算两个数值之间的差值

TSD的接口：
当前采集时间戳 本次采集和上次采集的数值差
"""
import sys
import urllib2

from argus_collector.collectors.common import *
from argus_collector.collectors.etc.flume_metric_conf import *

DATA_PATH = os.path.join(DATA_DIR, 'flume_metric.data')
TIME_INTERVAL = os.path.basename(os.path.dirname((os.path.abspath(__file__)))).strip()

CLUSTER_DATA_PATH = os.path.join(DATA_DIR, 'flume_cluster.data')
CLUSTER_START_TIME_PATH = os.path.join(DATA_DIR, 'flume_cluster_start_time.data')

DATA_CONTAINER = {}
START_TIME_CONTAINER = {}


def get_flume_data():
    """请求flume的API，获取JSON数据"""
    request_url = "http://{0}:{1}{2}".format(FLUME_HOST, FLUME_PORT, FLUME_URL_ENDPOINT)
    ret = urllib2.urlopen(request_url)
    if ret.code != 200:
        print >> sys.stderr, 'Could not get data from flume api! Request url: ' + request_url
        sys.exit()
    return ret.read()


def parse_json(json_str):
    """从JSON数据中提取用户配置的指标数值"""
    json_dict = json.loads(json_str)
    res = []
    for metric_name, search_path in FLUME_METRIS.iteritems():
        res.append((metric_name, search_from_path(json_dict, search_path)))
    return dict(res)


def search_from_path(data, search_path):
    """根据列表路径，从字典中提取值"""
    # 递归结束条件
    if not len(search_path) or not isinstance(data, (dict, list, tuple)):
        return data
    # 递归提取
    if isinstance(data, (dict, list, tuple)):
        return search_from_path(data[search_path[0]], search_path[1:])


def get_flume_agent(host, port, endpoint=FLUME_URL_ENDPOINT):
    """请求flume的API，获取JSON数据"""
    request_url = "http://{0}:{1}{2}".format(host, port, endpoint)
    # print(request_url)
    ret = urllib2.urlopen(request_url)
    if ret.code != 200:
        print >> sys.stderr, 'Could not get data from flume api! Request url: ' + request_url
        sys.exit()
    return ret.read()


def parse_agent(json_str, agent_metric):
    """从JSON数据中提取用户配置的指标数值"""
    json_dict = json.loads(json_str)
    res = []
    for metric_name, search_path in agent_metric.iteritems():
        res.append((metric_name, search_from_path(json_dict, search_path)))
    return dict(res)


def add_start_time(data):
    """
    {"host:port": timestamp}
    """

    for k, v in data.iteritems():
        START_TIME_CONTAINER[k] = v


def add_data(data):
    """
    {
        "host:port":{
            "metric1": value1,
            "metric2": value2,
        }
    }
    """
    for k, v in data.iteritems():
        DATA_CONTAINER[k] = v


def parse_config():
    """
    Construct agent info from FLUME_CLUSTER.

    While planning to support new annotation pattern, add it's parser here.
    """
    agents = []  # all agents in the task list should be a tuple (host, port, metric)
    for host, detail in FLUME_CLUSTER.iteritems():
        for p, m in detail.iteritems():
            if isinstance(p, int):  # single port & metric
                agents.append((host, p, SUPPORT_METRICS[m]))
            elif isinstance(p, str):  # port segment
                start, end = map(int, p.split('-'))
                port_count = end - start + 1
                if isinstance(m, int):  # port segment & single same metric
                    for i in range(start, end + 1):
                        agents.append((host, i, SUPPORT_METRICS[m]))
                elif isinstance(m, list):  # port segment & metric segment
                    if port_count == len(m):  # the quantity of port metric segment is equal
                        _ = zip([host for i in range(port_count)], [i for i in range(start, end + 1)],
                                [SUPPORT_METRICS[i] for i in m])
                        agents.extend(_)
                    # port counts does not match metric quantity
                    if port_count < len(m):
                        _ = zip([host for i in range(port_count)], [i for i in range(start, end + 1)],
                                [SUPPORT_METRICS[i] for i in m])
                        agents.extend(_)
                    if port_count > len(m):
                        new_m = m * (port_count / len(m) + 1)
                        _ = zip([host for i in range(port_count)], [i for i in range(start, end + 1)],
                                [SUPPORT_METRICS[i] for i in new_m])
                        agents.extend(_)
    return agents


def main():
    """"""
    # TODO: @hehao
    # 1) 支持采集多个flume源，多个host、port
    # 2）不同的host、port的flume数据源，通过一个tag来区分（ex: hostPort=localhost_9002）
    # 3）每次采集前检测flume是否重启过，如果重启过，需要重新初始化用于计算差值的数值
    if not FLUME_METRIS:
        sys.exit(0)

    current_time = int(time.time())
    if TIMESTAMP_ALIGN:
        send_time = current_time - current_time % int(TIME_INTERVAL)
    else:
        send_time = current_time

    flume_data_now = get_flume_data()
    res_now = parse_json(flume_data_now)

    last_data = get_last_data(DATA_PATH)
    if last_data is not None:
        last_time = last_data.keys()[0]
        res_last = last_data[last_time]
        # 计算差值
        for metric, value in res_now.iteritems():
            last_value = res_last.get(metric, None)
            if last_value is not None:
                print("{0} {1} {2}".format(
                    metric if not ALL_LOWER_CASE else metric.lower(), send_time, float(value) - float(last_value)
                ))

        sys.stdout.flush()

    save_data(DATA_PATH, res_now, current_time)


def flume_cluster_main():
    """
    Update flume cluster support, using new config anotation.

    Config:
    {
        host: {
            port: metric
            port_segment: metric_segment
        }
    } 
    
    CLUSTER_DATA_PATH:
    {
        "1505468652": {
            "localhost:20161": {
                "SINK.sink2.EventDrainSuccessCount": 48, 
                "SOURCE.src2.EventReceivedCount": 48
            }, 
            "127.0.0.1:20160": {
                "SINK.sink1.EventDrainSuccessCount": 36, 
                "SOURCE.src1.EventReceivedCount": 36
            }
        }
    }

    CLUSTER_START_TIME_PATH:
    {
        "1505468652": {
            "localhost:20161": "2333333333333323333333333333",
            "127.0.0.1:20160": "1505468524446"
        }
    }
    """
    if not FLUME_CLUSTER:
        sys.exit()

    current_time = int(time.time())

    last_data = get_last_data(CLUSTER_DATA_PATH)
    last_start_time = get_last_data(CLUSTER_START_TIME_PATH)

    last_start_time_key, last_data_key = None, None  # a timestamp str as the dict key
    if last_data:
        last_data_key = last_data.keys()[0]
    if last_start_time:
        last_start_time_key = last_start_time.keys()[0]

    agents = parse_config()
    for agent in agents:  # (host, port, metric)
        raw_str = get_flume_agent(*agent[:-1])
        # {'m1': 'v1', 'm2': 'v2', 'm3.StartTime': 'v3'}
        info = parse_agent(raw_str, agent[2])  # representing the new data

        # whether reboot or not
        rebooted = False
        store_key = '{0}:{1}'.format(*agent[:-1])  # the key used to store start time or data
        start_time_key = [i for i in agent[2].keys() if 'StartTime' in i][0]
        current_start_time = info.get(start_time_key)
        add_start_time({store_key: str(current_start_time)})

        if last_start_time_key:
            previous_start_time = last_start_time[last_start_time_key][store_key]
            if current_start_time != previous_start_time:
                rebooted = True

        if rebooted:
            print(store_key, 'has rebooted')
            temp = [(metric, info[metric]) for metric in agent[2].keys() if metric != start_time_key]
            temp = dict(temp)
            add_data({store_key: temp})
        else:
            temp = [(metric, info[metric]) for metric in agent[2].keys() if metric != start_time_key]
            temp = dict(temp)
            add_data({store_key: temp})
            if last_data_key:
                res_last = last_data[last_data_key]
                for metric, new_value in temp.iteritems():
                    last_value = res_last[store_key].get(metric, None)
                    if last_value is not None:
                        print("{0} {1} {2} {3}".format(
                            metric if not ALL_LOWER_CASE else metric.lower(), current_time,
                            float(new_value) - float(last_value), 'flume_agent=' + store_key.replace(':', '_')
                        ))

    save_data(CLUSTER_DATA_PATH, DATA_CONTAINER)
    save_data(CLUSTER_START_TIME_PATH, START_TIME_CONTAINER)


if __name__ == '__main__':
    # main()
    flume_cluster_main()
