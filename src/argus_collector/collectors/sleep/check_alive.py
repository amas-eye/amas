#!/usr/bin/env python
# coding=utf8
"""
这个脚本是用于采集机器存货与否
"""
import os
import time
import threading

if __name__ == "__main__":
    cmd = "cat /proc/uptime | awk {'print $1'}"
    cmd_result = os.popen(cmd)
    uptime_str = cmd_result.read()
    uptime = float(uptime_str.rstrip())
    ts = int(time.time())
    if uptime > 0:
        print "sys.machine.alive {ts} 1".format(ts=ts)
    
