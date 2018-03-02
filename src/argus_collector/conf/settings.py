"""
default settings
"""
OPEN_TSDB_HOST = 'localhost'
OPEN_TSDB_PORT = 4242

"""
in the agent manager part , you can add manager as you want
as long as following the rule is 
AGENT_MANAGER_HOSTx (x in here mean an interger)
AGENT_MANAGER_PORTx (x in here mean an interger)
and finally adding up the AGENT_MANAGER_TOTAL as the manager you have added
"""

AGENT_MANAGER_HOST1 = 'localhost'
AGENT_MANAGER_PORT1 = 8001

AGENT_MANAGER_HOST2 = '192.168.0.249'
AGENT_MANAGER_PORT2 =  8001

AGENT_MANAGER_TOTAL = 2


PUSH_STATUS_FREQUENCY = 1 * 60

CONFIG_SENDER_FREQUENCY = 5 * 60

PUSH_STATUS = True

LOG_LEVEL = 'DEBUG'  # DEBUG INFO WARN ERROR CRITICAL
LOG_FILE = ''  # defaults to logs/collector.log

TAGS = [
    # 'host=localhost',
]


DRY_RUN = False

# whether or not to deal with timestamp with millisecond precision
FLOAT_TIMESTAMP = False

#   dedupinterval: If a metric sends the same value over successive
#     intervals, suppress sending the same value to the TSD until
#     this many seconds have elapsed.  This helps graphs over narrow
#     time ranges still see timeseries with suppressed datapoints.
#   evictinterval: In order to implement the behavior above, the
#     code needs to keep track of the last value seen for each
#     combination of (metric, tags).  Values older than
#     evictinterval will be removed from the cache to save RAM.
#   Invariant: evictinterval > dedupinterval
#   units: seconds
DEDUP_INTERVAL = 0
EVICT_INTERVAL = 6000

# If we're running as root and this user exists, we'll drop privileges.
DROP_TO_USER = '_'


import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
