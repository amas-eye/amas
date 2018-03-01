# coding=utf8
"""
进程监控的配置
CONFIG = {
    "指标名": "grep指标名的shell指令"
}
"""
# 是否根据采集时间间隔转换时间，使得ECharts画图多个指标时x轴对齐
TIMESTAMP_ALIGN = True

CONFIG = {
    "sys.proc.python": "ps aux|grep python|grep -v grep|awk '{print $2}'"
}
