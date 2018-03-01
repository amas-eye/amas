# coding=utf-8
"""指标正常度统计

扫描当前的告警状态，统计包含了多少指标，得出异常指标数及其比例
"""

import json
import time

from collections import namedtuple

from argus_statistics.utils import (urlopen, get_client, send_to_db,
                                    OPENTSDB_HOST, OPENTSDB_PORT,)


def update_metric():
    """
    Support metric status for dashboard page.
    """

    fields = ['check_time', 'metrics', 'normal', 'error']  # current data model
    result = {f: None for f in fields}

    result['check_time'] = int(time.time())
    result['metrics'] = get_metrics_quantity()
    result['error'] = get_triggered_metrics_quantity()
    result['normal'] = result['metrics'] - result['error']
    send_to_db('argus-statistics', 'metric_stat', result)


def get_metrics_quantity(host: str= OPENTSDB_HOST,
                         port: int= OPENTSDB_PORT) -> int:
    """
    2 http requests to find out how many metrics existed in OpenTSDB currently.
    """

    host, port = host, port
    radix_url = f'http://{host}:{port}/api/stats'  # the url used to find used ids
    radix_raw = urlopen(radix_url,)
    radix_meta = json.load(radix_raw)
    radix = 9  # a base num add to real used ids in opentsdb

    for item in radix_meta:
        if item['metric'] == 'tsd.uid.ids-used':
            radix += int(item['value'])

    quantity_url = f'http://{host}:{port}/api/suggest?'
    params = {'type': 'metrics', 'max': radix}
    quantity_raw = urlopen(quantity_url, params)
    quantity = len(json.load(quantity_raw))

    return quantity


def get_triggered_metrics_quantity(db: str='argus-alert',
                                   strategy_coll: str='strategy') -> int:
    """
    Since we have independent alert module, here get the data from MongoDB.

    Hint:
        A trrigered strategy may use more than one metric.
    """

    client = get_client()  # get MongoDB client
    db = client[db]
    strategy_coll = db[strategy_coll]
    condition = {'status': 'alert'}

    _ = 'ignored'
    Strategy = namedtuple('Strategy', [_, _, _, 'tsd_rule', _, _, _, _],
                          rename=True)

    triggered_strategies = map(lambda x: Strategy._make(dict(x).values()), strategy_coll.find(condition))
    triggered_metrics = set()

    for strategy in triggered_strategies:
        if isinstance(strategy.tsd_rule['metric'], list):
            for metric in strategy.tsd_rule['metric']:
                triggered_metrics.add(metric)
        if isinstance(strategy.tsd_rule['metric'], str):
            triggered_metrics.add(strategy.tsd_rule['metric'])

    quantity = len(triggered_metrics)

    return quantity


if __name__ == '__main__':
    pass
