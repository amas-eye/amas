"""
default settings
"""
OPEN_TSDB_HOST = 'localhost'
OPEN_TSDB_PORT = 4242

AGENT_MANAGER_HOST = 'localhost'
AGENT_MANAGER_PORT = 8001

PUSH_STATUS_FREQUENCY = 1 * 60

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
