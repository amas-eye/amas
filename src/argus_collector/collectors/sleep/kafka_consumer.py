#!/usr/bin/env python
# coding=utf-8
"""作为消费者采集kafka队列的消息，处理后发送到tsd
"""
from kafka import KafkaConsumer
from argus_collector.collectors.etc.kafka_consumer_conf import *


def main():
    """"""
    consumer = KafkaConsumer(*KAFKA_TOPICS,
                             bootstrap_servers=KAFKA_SERVERS,
                             group_id=KAFAK_GROUP_ID
                             )
    for msg in consumer:
        print msg
        # TODO: deal with msg


if __name__ == '__main__':
    main()