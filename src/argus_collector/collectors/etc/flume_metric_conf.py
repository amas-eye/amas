# coding=utf8
"""
flume的度量监控数据采集的配置，配置在FLUME_METRICS变量中，key值是指标名，value值是读取数值的路径
例如，下面这个json中：
{
"a": {
        "b": 1,
        "c": {
            "d": 2
            },
        "e": [3, 4, 5]
    }
}

如需读取"b"的值，value配置读取路径为：["a", "b"];
如需读取"d"的值，value配置读取路径为：["a", "c", "d"];
如需读取"e"数组的第1个值(即3)，配置读取路径为：["a", "e", 0], 整数0代表数组的下标

key值作为上传到tsd的指标名，比如上传指标a.c.d：
FLUME_METRICS = {
    "a.c.d": ["a", "c", "d"],
}
"""

__all__ = ['FLUME_METRIS', 'TIMESTAMP_ALIGN', 'FLUME_HOST', 'FLUME_PORT','FLUME_URL_ENDPOINT','ALL_LOWER_CASE']

# json格式监控数据中的字段选择（大小写敏感）
FLUME_METRIS = {
    "SINK.sink1.EventDrainSuccessCount": ["SINK.sink1", "EventDrainSuccessCount"],
    "SOURCE.src1.EventReceivedCount": ["SOURCE.src1", "EventReceivedCount"],
    # "CHANNEL.ch1.test.haha": ["CHANNEL.ch1", "test", "haha", 0],
}

# 是否根据采集时间间隔转换时间，使得ECharts画图多个指标时x轴对齐
TIMESTAMP_ALIGN = True

# flume监控数据接口的ip、端口和uri
FLUME_HOST = "localhost"
FLUME_PORT = 20160
FLUME_URL_ENDPOINT = "/metrics"

# for flume cluster
SUPPORT_METRICS = {
    1: {
        "SINK.sink1.EventDrainSuccessCount": ["SINK.sink1", "EventDrainSuccessCount"],
        "SOURCE.src1.EventReceivedCount": ["SOURCE.src1", "EventReceivedCount"],
        "SINK.sink1.StartTime": ["SINK.sink1", "StartTime"]  # used to determine flume agent's start time
    },
    2: {
        "SINK.sink2.EventDrainSuccessCount": ["SINK.sink2", "EventDrainSuccessCount"],
        "SOURCE.src2.EventReceivedCount": ["SOURCE.src2", "EventReceivedCount"],
        "SINK.sink2.StartTime": ["SINK.sink2", "StartTime"]
    },
    3: {
        "SINK.sink3.EventDrainSuccessCount": ["SINK.sink3", "EventDrainSuccessCount"],
        "SOURCE.src3.EventReceivedCount": ["SOURCE.src3", "EventReceivedCount"],
        "SINK.sink3.StartTime": ["SINK.sink3", "StartTime"]
    },
    4: {
        "SINK.sink4.EventDrainSuccessCount": ["SINK.sink4", "EventDrainSuccessCount"],
        "SOURCE.src4.EventReceivedCount": ["SOURCE.src4", "EventReceivedCount"],
        "SINK.sink4.StartTime": ["SINK.sink4", "StartTime"]
    },
    5: {
        "SINK.sink5.EventDrainSuccessCount": ["SINK.sink5", "EventDrainSuccessCount"],
        "SOURCE.src5.EventReceivedCount": ["SOURCE.src5", "EventReceivedCount"],
        "SINK.sink5.StartTime": ["SINK.sink5", "StartTime"]
    },
    6: {
        "SINK.sink6.EventDrainSuccessCount": ["SINK.sink6", "EventDrainSuccessCount"],
        "SOURCE.src6.EventReceivedCount": ["SOURCE.src6", "EventReceivedCount"],
        "SINK.sink6.StartTime": ["SINK.sink6", "StartTime"]
    },
    7: {
        "SINK.sink7.EventDrainSuccessCount": ["SINK.sink7", "EventDrainSuccessCount"],
        "SOURCE.src7.EventReceivedCount": ["SOURCE.src7", "EventReceivedCount"],
        "SINK.sink7.StartTime": ["SINK.sink7", "StartTime"]
    }
}

# PLEASE FOLLOW THE ANOTATION!!!
FLUME_CLUSTER = {
        '127.0.0.1':{
            20160: 1  # port : metric
        },  # passed
        'localhost':{
            '20161-20163': 1,  # port from 20161 to 20163 both attach to metric 2. passed
            '20165-20167': [1, 2, 3],  # port segmet : metric segment i.e. 20165:1, 20166:2 20167:3
            # the count MUST be matched i.e. port_count = metric_count
            # '20171-20179': [1, 2, 3],  # 20171:1, 20172:2, 20173:3, 20174:1, 20175:2, 20176:3, 20177:1, 20178:2, 20179:3
        },
}

# 是否把发送到tsd的指标名都转换为小写
# 默认是False，保留指标名的大小写；改为True，则会进行转换
ALL_LOWER_CASE = False

# （弃用）两个采集时间点的时间间隔，单位：秒
# TIME_INTERVAL = 300
