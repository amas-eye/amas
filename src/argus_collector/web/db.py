#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Provide some necessary functionality.
"""

import os
import sqlite3
import json


from argus_collector.web.data.settings import DB, TABLE_SCHEMA
from argus_collector.web.status_code import *


METRIC_DEFAULT_DESCRIPTION = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data", "metric_note.json")


def get_db():
    """
    Return a sqlite3.Connection object
    """
    if _exist_table():
        pass
    else:
        _init_table()
    db = sqlite3.connect(DB)
    return db


def _exist_table():
    """
    Show whether or not the table exist in the sqlite3 db.
    """
    db = sqlite3.connect(DB)
    cursor = db.cursor()
    result = cursor.execute("select name from sqlite_master \
                            where type='table' and name=?;", ('metric',))
    exist = result.fetchone()
    db.close()
    if exist:
        return True
    else:
        return False


def _init_table():
    """
    Read the sql file and initial the table 'metric'.
    """
    try:
        with open(TABLE_SCHEMA, 'r') as _sql:
            sql = _sql.read()
            db = sqlite3.connect(DB)
            db.cursor().executescript(sql)
            db.commit()
            db.close()
    except Exception as e:
        return False


def is_existed(data):
    """
    Whether or not a metric_name already exist.
    """
    if data['metric_name'] in get_all_metrics():
        return True
    else:
        return False


def get_all_metrics():
    """Return a list containing all metrics(str) in local db."""
    db = get_db()
    cur = db.cursor()
    _sql = 'SELECT metric_name FROM metric'
    cur.execute(_sql)
    result = cur.fetchall()
    cur.close()
    db.close()
    if result:
        result =  map(' '.join, result)
        return result
    else:
        return result


def update(data):
    """
    Update  a row in the db, including descripton, tags, last_update.
    """
    if isinstance(data, dict):
        return update_single_record(data)
    elif isinstance(data, list):
        return update_multiple_records(data)


def is_valid(data):
    """Whether or not the data we recieved is valid, i.e. a dict containing the following 3 keys"""
    try:
        _m = data['metric_name']
        _d = data['description']
        _t = data['tags']
    except KeyError as e:
        return False
    except Exception as e:
        return False
    else:
        return True


def update_single_record(data):
    """handle front end request and update a record in local db."""
    if not is_valid(data):
        error = {
            'code': INVALID_JSON,
            'msg': 'Invalid JSON, check your json field <{0}>.'.format(data),
            'example': {
                'metric_name': '???',
                'description': '???',
                'tags': '???',
            }
        }
        return error

    if not is_existed(data):
        error = {
            'code': METRIC_NOT_FOUND,
            'msg': 'Check your metric_name <{0}>, it does not exist in the db'.format(
                data['metric_name'])
        }
        return error
    try:
        db = get_db()
        cur = db.cursor()
        metric_name = data['metric_name']
        description = data['description']
        tags = data['tags']
        _sql = 'UPDATE metric SET description = ?, tags = ? WHERE metric_name = ?;'
        cur.execute(_sql, (description, tags, metric_name))
        db.commit()
        cur.close()
        db.close()
        success = {
                'code': UPDATE_ACCEPTED,
                'updated': 1
        }
    except Exception as e:
        return {
                'code': UPDATE_FAILED,
                'msg': e
        }
    else:
        return success


def update_multiple_records(data):
    """Using post json as new record, return a refused list while encounter invalid json."""
    valid_data = filter(is_valid, data)  # valid data_set
    invalid_data = filter(lambda x: not is_valid(x), data)  # invalid data set
    existed_data = filter(is_existed, valid_data)  # both valid and existed so update them
    not_existed_data = filter(lambda x: not is_existed(x), valid_data)  # valid but is not existed

    try:
        db = get_db()
        cur = db.cursor()
        _sql = 'UPDATE metric SET description=?, tags=? WHERE metric_name = ?;'
        purchases = [(d['description'], d['tags'], d['metric_name']) for d in existed_data]
        cur.executemany(_sql,  purchases)
        db.commit()
        cur.close()
        db.close()
    except Exception as e:
        error = {
                'code': DB_ERROR,
                'msg': e
        }
        return error

    result = {}
    if existed_data:
        result['code'] = UPDATE_UNCOMPLETED
        result['updated'] = len(existed_data)
        result['refused'] = len(invalid_data)
        result['refused_list'] = invalid_data
    else:
        result['code'] = UPDATE_FAILED
        result['updated'] = len(existed_data)

    result['refused'] = len(invalid_data)
    result['refused_list'] = invalid_data
    result['unknown'] = len(not_existed_data)
    result['unknown_list'] = not_existed_data

    if len(existed_data) == len(data):
        result['code'] = UPDATE_ACCEPTED
        result['updated'] = len(existed_data)
    return result


def get_records(offset, limit):
    """
    Return the data set in a specific arragement.
    Omit the `limit` and `offset` when execut the SQL statement, \
    then hanlde it  via Python Slice.
    """
    check_result = check_param(limit, offset)
    if check_result['code'] == REQUEST_PARAM_INVAILD:
        return check_result

    offset = int(offset)
    limit = int(limit)
    SUBRESULT = slice(offset, offset+limit)  # a little trick

    # _sql = 'SELECT metric_name, description, tags, last_update FROM metric;'
    _sql = ('SELECT metric_name, description, tags, last_update FROM metric '
            'ORDER BY last_update DESC;')

    result = []

    try:
        db = get_db()
        cur = db.cursor()
        cur.execute(_sql)
        for i in cur.fetchall():
            r = {}
            r['metric_name'] = i[0]
            r['description'] = i[1] if i[1] else get_default_description(i[0])
            r['tags'] = i[2]
            r['last_update'] = i[3]
            result.append(r)
    except Exception as e:
        return {
                'code': DB_ERROR,
                'msg': e
        }
    else:
        return {
                'code': CODE_OK,
                'data': result[SUBRESULT],
                'total': len(result)
        }


def get_records_via_kw(kw, offset, limit):
    """
    Fetch all records and then hanlde the `kw` via Python Slice.
    """
    check_result = check_param(limit, offset)
    if check_result['code'] == REQUEST_PARAM_INVAILD:
        return check_result

    offset = int(offset)
    limit = int(limit)
    SUBRESULT = slice(offset, offset+limit)

    _sql = ('SELECT metric_name, description, tags, last_update FROM metric '
            'ORDER BY last_update DESC;')
    result = []

    try:
        db = get_db()
        cur = db.cursor()
        cur.execute(_sql)
        for i in cur.fetchall():
            if str(kw) in i[0]:  # such as 'python' in 'sys.process.python'
                r = {}
                r['metric_name'] = i[0]
                r['description'] = i[1] if i[1] else get_default_description(i[0])
                r['tags'] = i[2]
                r['last_update'] = i[3]
                result.append(r)
    except Exception as e:
        return {
                'code': DB_ERROR,
                'msg': e
        }
    else:
        return {
                'code': CODE_OK,
                'data': result[SUBRESULT],
                'total': len(result)
        }


def check_param(limit, offset):
    try:
        if int(limit) < -1 or int(offset) < 0:
            return {
                    'code': REQUEST_PARAM_INVAILD,
                    'msg': 'check out your limit and offset params'
            }
    except Exception as e:
            return {
                    'code': REQUEST_PARAM_INVAILD,
                    'msg': 'check out your limit and offset params'
            }
    else:
        return {
                'code': 'True'
        }


def get_default_description(metric_name):
    with open(METRIC_DEFAULT_DESCRIPTION) as f:
        ddj = json.load(f)
    for c in ddj:
        for _k, _v in ddj[c].iteritems():
            if metric_name == _k:
                return _v


def insert_many(new_dict):
    db = get_db()
    cur = db.cursor()
    purchases = [(None, m, None, None, t) for m, t in new_dict]
    cur.executemany('INSERT INTO metric VALUES (?,?,?,?,?)', purchases)
    db.commit()
    cur.close()
    db.close()


def update_many(existed_dict):
    db = get_db()
    cur = db.cursor()
    _sql = 'UPDATE metric SET last_update = ? WHERE metric_name = ?;'
    purchases = [(t, m) for m, t in existed_dict if t != -2]  # -2 means the latest request don not return anything so do noting to the records in local db
    cur.executemany(_sql,  purchases)
    db.commit()
    cur.close()
    db.close()


if __name__ == '__main__':
    print(get_default_description("sys.network.rtt"))
