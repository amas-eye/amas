# coding=utf8
"""
网卡采集器的配置
"""

Property = ['NETWORK_INTERFACE_CARD','TIMESTAMP_ALIGN','FIELDS']

# 网卡，可以是单个字符串，也可以是一个数组（同时采集多个网卡）
NETWORK_INTERFACE_CARD = ['bond0']

# 是否根据采集时间间隔转换时间，使得ECharts画图多个指标时x轴对齐
TIMESTAMP_ALIGN = True

# 需要采集的网卡字段
FIELDS = {
    "receive": ["bytes"],
    "transmit": ["bytes"]
}
