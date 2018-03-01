#!/usr/bin/python
# coding=utf8
"""
把flume采集到的慢sql日志翻译成json的格式后存入到mongodb里面
"""
import re

import pymongo
from kafka import KafkaConsumer

topic = "mysql_slow_log"
bootstrap_server_ip = ""  # watch your kafka consumer bootstrap
client_id = "ray"  # change whatever name you want
mongoip = ""  # mongodb ip or mongodb hostname
db = ""  # mongodb database to save data
collection = ""  # mongodb collection


def send_to_mongo(sdict, mongoip, dbname, collection):
    client = pymongo.MongoClient(mongoip, 27017)
    db = client.dbname
    collection_list = db.collection_names()
    if not collection in collection_list:
        db.create_collection(collection)
    result = db.collection.insert_one(sdict)
    if result:
        print "insert success"
    else:
        print "fail"


def parse_slow_log(line, count, sdict):
    if re.match(r"# Time:", line) and count == 0:
        line_split = line.split("# Time: ")
        time = line_split[1]
        sdict["time"] = time
        count += 1
        return [sdict, count]
    elif re.match(r"# User", line):
        line_split = line.split("# User@Host: ")
        line1_split = line_split[1]
        user = line1_split.split("[]")[0]
        sdict["user"] = user
        count += 1
        return [sdict, count]
    elif re.match(r"# Query_time", line):
        line_split = line.split(" ", 3)
        query_time = line_split[2]
        sdict["query_time"] = query_time
        count += 1
        return [sdict, count]
    elif re.match(r"select|update|delete|insert", line):
        sql = line
        sdict["sql"] = sql
        if count == 3:
            send_to_mongo(sdict, mongoip, db, collection)
            sdict = {}
            count = 0
            return [sdict, count]
    else:
        return [sdict, count]


if __name__ == "__main__":
    consumer = KafkaConsumer(topic,
                             bootstrap_servers=bootstrap_server_ip,
                             client_id=client_id
                             )
    count = 0
    sdict = {}
    for msg in consumer:
        value = msg.__getattribute__("value")
        sdict, count = parse_slow_log(value, count, sdict)
