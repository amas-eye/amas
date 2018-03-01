#!/usr/bin/python
# coding=utf8
"""
        Mbean: kafka.server:type=KafkaServer,name=BrokerState
        - kafka.broker.brokerstate [value]
        Mbean: kafka.server:type=KafkaServer,name=ClusterId
        - kafka.broker.clusterid    [value]
        Mbean: kafka.server:type=DelayedOperationPurgatory,name=NumDelayedOperations,delayedOperation=Fetch
        - kafka.broker.delayfetch   [value]
        Mbean: kafka.server:type=DelayedOperationPurgatory,name=NumDelayedOperations,delayedOperation=Produce
        - kafka.broker.delayproduce [value]
        Mbean: kafka.server:type=DelayedOperationPurgatory,name=NumDelayedOperations,delayedOperation=Heartbeat
        - kafka.broker.delayheartbeat [value]
        Mbean: kafka.server:type=DelayedOperationPurgatory,name=NumDelayedOperations,delayedOperation=Topic
        - kafka.broker.delaytopic   [value]
        Mbean: kafka.server:type=DelayedOperationPurgatory,name=NumDelayedOperations,delayedOperation=Rebalance
        - kafka.broker.delayrebalance [value]
        Mbean: kafka.server:type=ReplicaManager,name=PartitionCount
        - kafka.broker.partitioncount [value]
        Mbean: kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions
        - kafka.broker.underreplicatedpartitions [value]
        Mbean: kafka.server:type=ReplicaManager,name=IsrExpandsPerSec
        - kafka.broker.isrexpandspeed [count]
        Mbean: kafka.server:type=ReplicaManager,name=IsrShrinksPerSec
        - kafka.broker.isrshrinkspeed [count]

        node = topic
        Mbean: kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec
        - kafka.broker.topic.byteinpersecond [count]
        Mbean: kafka.server:type=BrokerTopicMetrics,name=BytesOutPerSec
        - kafka.broker.topic.byteoutpersecond [count]
        Mbean: kafka.server:type=BrokerTopicMetrics,name=BytesRejectedPerSec
        - kafka.broker.topic.byterejectpersecond [count]
        Mbean: kafka.server:type=BrokerTopicMetrics,name=TotalFetchRequestsPerSec
        - kafka.broker.topic.totalfetchrequestpersecond [count]
        Mbean: kafka.server:type=BrokerTopicMetrics,name=TotalProduceRequestsPerSec
        - kafka.broker.topic.totalproducerequestpersecond [count]

     node = controller
        Mbean: kafka.controller:type=KafkaController,name=OfflinePartitionsCount
        - kafka.controller.offlinepartitioncount [value]
        Mbean: kafka.controller:type=KafkaController,name=ActiveControllerCount
        - kafka.controller.activecontrollerconut [value]
        Mbean: kafka.controller:type=ControllerStats,name=UncleanLeaderElectionsPerSec
        - kafka.controller.uncleanLeaderElection [count]
        # Mbean: kafka.controller:type=ControllerStats,name=LeaderElectionRateAndTimeMs
        # - kafka.controller.leaderelectiontime

//TODO 需要进行对producer和consumer的采集，

"""
import urllib2
import sys
import json
import time

from argus_collector.collectors.etc.kafka_conf import *


def main():
    def get_response(jurl, post_data):
        try:
            ret = urllib2.urlopen(urllib2.Request(url=jurl, data=json.dumps(post_data)))
            if ret.code == 200:
                res = json.loads(ret.read())
                if res['status'] == 200:
                    # print res['value']
                    return res['value']
                else:
                    print >> sys.stderr, 'status: ', res['status']
                    print >> sys.stderr, 'error: ', res['error']
                    print >> sys.stderr, 'error type: ', res['error_type']
                    print >> sys.stderr, 'stacktrace: ', res['stacktrace']
            else:
                print >> sys.stderr, ret.code, ret.msg
        except urllib2.URLError:
            print "需要检查你的jolokia配置"

    def get_data_proxy(kh, jmx_port, mbean_name, att, jolokia_url):
        params = {
            "type": query_type,
            "mbean": mbean_name,
            "attribute": att,
            "target": {
                "url": "service:jmx:rmi:///jndi/rmi://{kafka_host}:{jmx_port}/jmxrmi".format(
                    kafka_host=kh, jmx_port=jmx_port
                ),
                "user": "",
                "password": "",
            }
        }
        value = get_response(jolokia_url, params)
        return value

    def get_data_local(mbean_name, att, jolokia_url):

        params = {
            "type": query_type,
            "mbean": mbean_name,
            "attribute": att,
        }

        value = get_response(jolokia_url, params)
        return value

    query_type = "read"
    jolokia_url_proxy = "http://{th}:{tp}/{jr}/".format(th=TOMCAT_HOST,
                                                        tp=TOMCAT_PORT,
                                                        jr=JOLOKIA_ROUTE
                                                        )
    jolokia_url_local = "http://127.0.0.1:{jp}/{jr}/".format(jp=JOLOKIA_PORT,
                                                             jr=LOCAL_JOLOKIA_ROUTE,
                                                             )

    count_mbean_dict = {
        "attr": "Count",
        "kafka.broker.topic.byteinpersecond": "kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec",
        "kafka.broker.topic.byteoutpersecond": "kafka.server:type=BrokerTopicMetrics,name=BytesOutPerSec",
        "kafka.broker.topic.byterejectpersecond": "kafka.server:type=BrokerTopicMetrics,name=BytesRejectedPerSec",
        "kafka.broker.topic.totalfetchrequestpersecond": "kafka.server:type=BrokerTopicMetrics,name=TotalFetchRequestsPerSec",
        "kafka.broker.topic.totalproducerequestpersecond ": "kafka.server:type=BrokerTopicMetrics,name=TotalProduceRequestsPerSec",
        "kafka.controller.uncleanLeaderElection": "kafka.controller:type=ControllerStats,name=UncleanLeaderElectionsPerSec",
        "kafka.broker.isrexpandspeed": "kafka.server:type=ReplicaManager,name=IsrExpandsPerSec",
        "kafka.broker.isrshrinkspeed": "kafka.server:type=ReplicaManager,name=IsrShrinksPerSec",
        "kafka.broker.topic.messageinrate": "kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec",
    }

    value_mbean_dict = {
        "attr": "Value",
        "kafka.broker.brokerstate": "kafka.server:type=KafkaServer,name=BrokerState",
        "kafka.broker.delayfetch": "kafka.server:type=DelayedOperationPurgatory,name=NumDelayedOperations,delayedOperation=Fetch",
        "kafka.broker.delayproduce": "kafka.server:type=DelayedOperationPurgatory,name=NumDelayedOperations,delayedOperation=Produce",
        "kafka.broker.delayheartbeat": "kafka.server:type=DelayedOperationPurgatory,name=NumDelayedOperations,delayedOperation=Heartbeat",
        # "kafka.broker.delaytopic": "kafka.server:type=DelayedOperationPurgatory,name=NumDelayedOperations,delayedOperation=Topic",
        "kafka.broker.delayrebalance": "kafka.server:type=DelayedOperationPurgatory,name=NumDelayedOperations,delayedOperation=Rebalance",
        "kafka.broker.partitioncount": "kafka.server:type=ReplicaManager,name=PartitionCount",
        "kafka.broker.underreplicatedpartitions": "kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions",
        "kafka.broker.maxlagmessages": "kafka.server:type=ReplicaFetcherManager,name=MaxLag,clientId=Replica",
        "kafka.broker.networkidlerate": "kafka.network:type=SocketServer,name=NetworkProcessorAvgIdlePercent",
    }

    metric_list = [value_mbean_dict, count_mbean_dict]

    for metrics in metric_list:
        ts = int(time.time())
        attr = metrics["attr"]
        del (metrics["attr"])
        if MODE == "PROXY":
            for host in KAFKA_HOST:
                for metric, mbean in metrics.items():
                    value = get_data_proxy(host, KAFKA_JMXPORT, mbean, attr, jolokia_url_proxy)
                    print "{m} {t} {v}".format(m=metric, t=ts, v=value)
        else:
            for metric, mbean in metrics.items():
                value = get_data_local(mbean, attr, jolokia_url_local)
                print "{m} {t} {v}".format(m=metric, t=ts, v=value)

        metrics["attr"] = attr


if __name__ == "__main__":
    sys.exit(main())
