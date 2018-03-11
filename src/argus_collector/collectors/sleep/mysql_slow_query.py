#!/usr/bin/python
# coding=utf8
"""
这个脚本是用于对慢sql语句进行提取反馈到监控信息中
默认前提，需要mysql 全局打开set global profiling=1
并且需要打开slow_query_log选项
目前感觉应该做成api
流程如下：
从slow_query_log定时读取一段时间以内的慢sql日志，然后在此api中
放入慢sql语句，从而获得每个sql语句最慢的部分

e.g
第一步： 获取慢sql语句
第二部执行 慢sql语句 ，获取总时间

第三部 通过搜索慢sql语句，进行show profile for query 序号（通过慢sql进行 query序号的匹配）
{u'Duration': Decimal('0.000064'), u'Status': 'starting'},
 {u'Duration': Decimal('0.000003'), u'Status': 'checking permissions'},
 {u'Duration': Decimal('0.000001'), u'Status': 'checking permissions'},
 {u'Duration': Decimal('0.000003'), u'Status': 'checking permissions'},
 {u'Duration': Decimal('0.000013'), u'Status': 'Opening tables'},
 {u'Duration': Decimal('0.000020'), u'Status': 'init'},
 {u'Duration': Decimal('0.000007'), u'Status': 'System lock'},
 {u'Duration': Decimal('0.000008'), u'Status': 'optimizing'},
 {u'Duration': Decimal('0.000029'), u'Status': 'statistics'},
 {u'Duration': Decimal('0.000012'), u'Status': 'preparing'},
 {u'Duration': Decimal('0.000018'), u'Status': 'Creating tmp table'},
 {u'Duration': Decimal('0.000004'), u'Status': 'Sorting result'},
 {u'Duration': Decimal('0.000001'), u'Status': 'executing'},
 {u'Duration': Decimal('0.028234'), u'Status': 'Sending data'},
 {u'Duration': Decimal('0.004765'), u'Status': 'converting HEAP to ondisk'},
 {u'Duration': Decimal('0.894775'), u'Status': 'Sending data'},
 {u'Duration': Decimal('0.865621'), u'Status': 'Creating sort index'},
 {u'Duration': Decimal('0.000009'), u'Status': 'end'},
 {u'Duration': Decimal('0.000007'), u'Status': 'query end'},
 {u'Duration': Decimal('0.000257'), u'Status': 'removing tmp table'},
 {u'Duration': Decimal('0.000003'), u'Status': 'query end'},
 {u'Duration': Decimal('0.000005'), u'Status': 'closing tables'},
 {u'Duration': Decimal('0.000013'), u'Status': 'freeing items'},
 {u'Duration': Decimal('0.000031'), u'Status': 'logging slow query'},
 {u'Duration': Decimal('0.000009'), u'Status': 'cleaning up'}]

然后只返回前五个因素

"""


import threading

