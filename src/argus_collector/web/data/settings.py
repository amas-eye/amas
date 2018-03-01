#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


OPEN_TSDB_HOST = '132.122.70.138'
OPEN_TSDB_PORT = 4242

DB = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.db')
TABLE_SCHEMA = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            'metric.sql')
API_LOG = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'api.log')
UPDATE_LOG = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'update.log')

DB_UPDATE_INTERVAL = 5 * 60
DB_UPDATE_CONCURRENCY = 10 # how many threads you want use in update process

if __name__ == '__main__':
    print(OPEN_TSDB_HOST, OPEN_TSDB_PORT, DB, TABLE_SCHEMA)
