#!/usr/bin/python
# This 'onload' function will be called by tcollector when it starts up.
# You can put any code here that you want to load inside the tcollector.
# This also gives you a chance to override the options from the command
# line or to add custom sanity checks on their values.
# You can also use this to change the global tags that will be added to
# every single data point.  For instance if you have multiple different
# pools or clusters of machines, you might wanna lookup the name of the
# pool or cluster the current host belongs to and add it to the tags.
# Throwing an exception here will cause the tcollector to die before it
# starts doing any work.
# Python files in this directory that don't have an "onload" function
# will be imported by tcollector too, but no function will be called.
# When this file executes, you can assume that its directory is in
# sys.path, so you can import other Python modules from this directory
# or its subdirectories.
import os
import sys
import logging
from argus_collector.conf import settings

LOG = logging.getLogger('tcollector')


def onload(options, tags):
    """Function called by tcollector when it starts up.

    Args:
        options: The options as returned by the OptionParser.
        tags: A dictionnary that maps tag names to tag values.
    """
    LOG.info('tcollector starting to execute onload()...')
    LOG.info('[options]: %s; [tags]: %s' % (str(options), str(tags)))


def get_defaults():
    """Configuration values to use as defaults in the code

        This is called by the OptionParser.
    """

    default_cdir = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'collectors')

    defaults = {
        'host': settings.OPEN_TSDB_HOST,
        'port': settings.OPEN_TSDB_PORT,

        'dryrun': settings.DRY_RUN,

        'logfile': settings.LOG_FILE if settings.LOG_FILE else os.path.join(settings.BASE_DIR, 'logs',
                                                                        'collector.log'),
        'loglevel': settings.LOG_LEVEL,

        'tags': settings.TAGS,

        'evictinterval': settings.EVICT_INTERVAL,
        'dedupinterval': settings.DEDUP_INTERVAL,

        'verbose': False,
        'no_tcollector_stats': True,
        'allowed_inactivity_time': 60 * 60,
        'maxtags': 8,
        'max_bytes': 64 * 1024 * 1024,
        'http_password': False,
        'reconnectinterval': 0,
        'http_username': False,
        'pidfile': os.path.join(settings.BASE_DIR, 'collector.pid'),
        'http': False,
        'remove_inactive_collectors': False,
        'backup_count': 1,
        'cdir': default_cdir,
        'ssl': False,
        'stdin': False,
        'daemonize': False,
        'hosts': False
    }

    return defaults


if __name__ == '__main__':
    print get_defaults().get('logfile')
