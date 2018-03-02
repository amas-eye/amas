#!/usr/bin/env python
"""network interface stats for TSDB"""

import re
import sys
import time

from argus_collector import utils

interval = 15  # seconds

# /proc/net/dev has 16 fields, 8 for receive and 8 for transmit,
# defined below.
# So we can aggregate up the total bytes, packets, etc
# we tag each metric with direction=in or =out
# and iface=

# The new naming scheme of network interfaces
# Lan-On-Motherboard interfaces
# em<port number>_< virtual function instance / NPAR Index >
#
# PCI add-in interfaces
# p<slot number>p<port number>_<virtual function instance / NPAR Index>


FIELDS = ("bytes", "packets", "errs", "dropped",
          "fifo.errs", "frame.errs", "compressed", "multicast",
          "bytes", "packets", "errs", "dropped",
          "fifo.errs", "collisions", "carrier.errs", "compressed")


def main():
    """ifstat main loop"""

    f_netdev = open("/proc/net/dev")
    utils.drop_privileges()

    # We just care about ethN and emN interfaces.  We specifically
    # want to avoid bond interfaces, because interface
    # stats are still kept on the child interfaces when
    # you bond.  By skipping bond we avoid double counting.
    while True:
        f_netdev.seek(0)
        ts = int(time.time())
        for line in f_netdev:
            m = re.match(r'''
                \s+
                (
                    eth?\d+ |
                    em\d+_\d+/\d+ | em\d+_\d+ | em\d+ |
                    p\d+p\d+_\d+/\d+ | p\d+p\d+_\d+ | p\d+p\d+ |
                    (?:   # Start of 'predictable network interface names'
                        (?:en|sl|wl|ww)
                        (?:
                            b\d+ |           # BCMA bus
                            c[0-9a-f]+ |     # CCW bus group
                            o\d+(?:d\d+)? |  # On-board device
                            s\d+(?:f\d+)?(?:d\d+)? |  # Hotplug slots
                            x[0-9a-f]+ |     # Raw MAC address
                            p\d+s\d+(?:f\d+)?(?:d\d+)? | # PCI geographic loc
                            p\d+s\d+(?:f\d+)?(?:u\d+)*(?:c\d+)?(?:i\d+)? # USB
                         )
                    )
                ):(.*)''', line, re.VERBOSE)
            if not m:
                continue
            intf = m.group(1)
            stats = m.group(2).split(None)

            def direction(i):
                if i >= 8:
                    return "out"
                return "in"

            for i in xrange(16):
                print("proc.net.%s %d %s iface=%s direction=%s"
                      % (FIELDS[i], ts, stats[i], intf, direction(i)))

        sys.stdout.flush()
        time.sleep(interval)


if __name__ == "__main__":
    sys.exit(main())
