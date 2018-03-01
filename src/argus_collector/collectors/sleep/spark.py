#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#     Filename @  spark.py
#       Author @  gouhao
#  Create date @  2017-07-27

"""
Some useful metrics in spark job, see more details in ../etc/spark_conf.py or doc/Metrics.md

---both status
spark.application.counts        attached tag: stauts[completed|running
spark.application.duration      attached tag: status[completed|runnning], appId,
---running applications only
spark.application.taskComplRate     attached tag: appId,            
spark.application.activetask	    attached tag: appId, jobId
spark.application.failedtask	    attached tag: appId, jobId
spark.application.completedtask     attached tag: appId, jobId
---completed application only
spark.executor.gctime       attached tag: appId, executorId
spark.executor.duration     attached tag: appId, executorId
"""

import json
import urllib2
import urllib
import time
import socket
from argus_collector.collectors.etc.spark_conf import *

running = set()
completed = {}


def get_counts():
    """
    Get the quantity of either running or completed applications
    """
    request_url = "http://{0}:{1}/api/v1/applications".format(SPARK_HISTORY_SERVER_HOST, SPARK_HISTORY_SERVER_PORT)

    origin_response = urllib2.urlopen(request_url)
    response_content = origin_response.read()
    # applications is a list which last few items' status is running
    applications = json.loads(response_content)

    timestamp = time.time()
    completed_count = running_count = 0

    for app in applications:
        if app["attempts"][0]["completed"]:
            completed_count += 1
        else:
            running_count += 1
    print_metric("spark.application.count", timestamp, completed_count, tag="status=completed")
    print_metric("spark.application.count", timestamp, running_count, tag="status=running")


def get_completed_durations():
    """
    Get the completed applications' duration.
    A special query parameter is minEndDate=2015-02-14T16:30:45.000GMT.
    Default minEndDate is None, that means fetch the whole applications.
    Can specify it by changing the ../data/spark.data
    """
    if not os.path.exists(LAST_TIME_PATH):
        last_time = ""
    else:
        try:
            with open(LAST_TIME_PATH, "r") as f:
                last_time = f.readlines()[0].strip()
        except IndexError:
            last_time = ""

    if last_time:
        query_parameters = urllib.urlencode({"minEndDate": last_time, "status": "completed"})
    else:
        query_parameters = ""

    base_url = "http://{0}:{1}/api/v1/applications".format(SPARK_HISTORY_SERVER_HOST, SPARK_HISTORY_SERVER_PORT)
    request_url = base_url + "?" + query_parameters

    origin_response = urllib2.urlopen(request_url)
    response_content = origin_response.read()
    applications = json.loads(response_content)

    for app in applications:
        appId = app["id"]
        # appName = app["name"]
        starttime = int(app["attempts"][0]["startTimeEpoch"])

        completed[app["id"]] = app["attempts"][0]["startTimeEpoch"]
        duration = app["attempts"][0]["duration"]
        status = "completed"

        # Use the applications" start time as the timestamp field in a data point
        print_metric("spark.application.duration", starttime, duration, tag="status=%s appId=%s" % (status, appId))

    # Save the last completed application"s completed time
    with open(LAST_TIME_PATH, "w") as f:
        f.write(applications[0]["attempts"][0]["endTime"])


def get_running_durations():
    """
    Get running applications' duration.
    """
    base_url = "http://{0}:{1}/api/v1/applications".format(SPARK_HISTORY_SERVER_HOST, SPARK_HISTORY_SERVER_PORT)
    request_url = base_url + "?" + "status=running"

    origin_response = urllib2.urlopen(request_url)
    response_content = origin_response.read()
    applications = json.loads(response_content)

    for app in applications:
        appId = app["id"]
        running.add(app["id"])
        starttime = app["attempts"][0]["startTimeEpoch"]
        formatted_start_time = int(str(app["attempts"][0]["startTimeEpoch"])[:10])
        duration = int((time.time() - formatted_start_time) * 1000)
        status = "running"
        print_metric("spark.application.duration", starttime, duration, tag="status=%s appId=%s" % (status, appId))


def get_tasks():
    """
    Get info about specific application which is running. 
    May be inaccurate beacasuse in a very short time the app in running set can be completed
    """

    if not running:
        return

    for app in running:
        request_url = "http://{0}:{1}/api/v1/applications/{2}/jobs/?status=running". \
            format(SPARK_HOST, SPARK_RUNNING_PORT, app)
        # Whether the running rest api server is online
        try:
            origin_response = urllib2.urlopen(request_url)
            response_content = origin_response.read()
            jobs = json.loads(response_content)
        except socket.error:
            continue

        for job in jobs:
            timestamp = int(time.time())
            jobId = job["jobId"]
            activeTasks = job["numActiveTasks"]
            completedTasks = job["numCompletedTasks"]
            failedTasks = job["numFailedTasks"]
            # tasks = job["numTasks"]
            # rate = float(completedTasks) / float(tasks)

            print_metric("spark.application.activetask", timestamp, activeTasks, tag="appId=%s jobId=%s" % (app, jobId))
            print_metric("spark.application.failedtask", timestamp, failedTasks, tag="appId=%s jobId=%s" % (app, jobId))
            print_metric("spark.application.completedtask", timestamp, completedTasks,
                         tag="appId=%s jobId=%s" % (app, jobId))


def get_executors():
    """
    Get the specific application's run information.
    """

    for app, start_time in completed.iteritems():
        request_url = "http://{0}:{1}/api/v1/applications/{2}/executors".format(SPARK_HISTORY_SERVER_HOST,
                                                                                SPARK_HISTORY_SERVER_PORT, app)

        origin_response = urllib2.urlopen(request_url)
        response_content = origin_response.read()
        executors = json.loads(response_content)
        for executor in executors:
            if executor["id"] == "driver":
                continue
            totalTasks = executor["totalTasks"]
            if totalTasks == 0:
                # Task error
                continue

            # completedTasks = executor["completedTasks"]
            # rate = float(completedTasks) / float(totalTasks)
            # isActive = executor["isActive"]
            # hostPort = executor["hostPort"]
            _id = executor["id"]
            totalDuration = executor["totalDuration"]
            totalGCTime = executor["totalGCTime"]

            # print_metric("spark.executor.completedrate", timestamp, rate, tag="appId=%s executorId=%s" %(app, _id) )
            print_metric("spark.executor.gctime", start_time, totalGCTime, tag="appId=%s executorId=%s" % (app, _id,))
            print_metric("spark.executor.duration", start_time, totalDuration,
                         tag="appId=%s executorId=%s" % (app, _id,))


def print_metric(metric, timestamp, value, tag=""):
    """
    Format the metric output.
    """
    print "%s %d %s %s" % (metric, int(timestamp), value, tag)


def format_time(timestamp):
    """
    Convert a timestamp digit to the formatted string used in query parameter.
    """
    s = int(timestamp)
    _ms = timestamp - s
    ms = int(_ms * 1000)
    ft = "{0}.{1:03d}".format(time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(s)), ms) + "GMT"
    return ft


def main():
    get_counts()
    get_completed_durations()
    get_running_durations()
    get_executors()
    get_tasks()


if __name__ == "__main__":
    main()
