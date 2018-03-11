# coding= utf8
"""
本文件需要进行指定kafka host、port
Jolokia host、port
还需指定kafka采集器的运行模式 Jolokia代理采集模式为PROXY， 本机部署采集的为LOCAL
JOLOKIA_PORT参数是用于Local模式的采集
"""

KAFKA_PORT = 9092
KAFKA_HOST = ['127.0.0.1']
KAFKA_JMXPORT = 1099
TOMCAT_HOST = '127.0.0.1'
TOMCAT_PORT = 8080
JOLOKIA_ROUTE = 'jolokia-war-1.3.7'

MODE = "LOCAL"

JOLOKIA_PORT = 8778
LOCAL_JOLOKIA_ROUTE = "jolokia"
