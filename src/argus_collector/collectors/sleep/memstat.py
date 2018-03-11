#!/usr/bin/env python
"""disk space and inode counts for TSDB """

# mem.bytes.memtotal
# mem.bytes.memfree
# mem.bytes.memavailable
# mem.bytes.buffers
# mem.bytes.cached
# ...


import sys
import time
from argus_collector import utils


def main():
    """check memory usage"""
    try:
        f_meminfo = open("/proc/meminfo", "r")
    except IOError as e:
        utils.err("error: can't open /proc/mounts: %s" % e)
        return 13  # Ask tcollector to not respawn us

    utils.drop_privileges()

    ts = int(time.time())
    total, free, buffers, cached = (0 for i in range(4))
    for line in f_meminfo.readlines():
        'MemTotal:        8055400 kB\n',
        'MemFree:         6529100 kB\n',
        'MemAvailable:    6965352 kB\n',
        'Buffers:           61824 kB\n',
        'Cached:           609784 kB\n',
        try:
            _info, _value, _unit = line.strip().split(None)
        except ValueError as e:
            _info, _value = line.strip().split(None)
        info = _info[:-1].lower()
        # coefficient is 1024 
        value = int(_value) * 1024
        if info == 'memtotal':
            total = value
        if info == 'memfree':
            free = value
        if info == 'buffers':
            buffers = value
        if info == 'cached':
            cached = value
        print("mem.bytes.%s %d %s" % (info, ts, value))
    used = total - free - buffers - cached
    print("mem.bytes.used %d %s" % (ts, used))
    f_meminfo.close()


if __name__ == "__main__":
    sys.exit(main())
