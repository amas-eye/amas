# coding=utf-8
"""基本告警的具体实现
"""
import json

import requests

from argus_alert.core.inspect.strategy_handler import IHandler, register_handler
from argus_alert.core.utils.log import timed_logger

LOG = timed_logger()


@register_handler
class BasicAlert(BaseAlert):
    """基础告警
    - 过去N时段、某指标、聚合值、和阈值对比
    """
    TYPE = 'basic'  # 大小写不敏感

    def __init__(self, *args, **kwargs):
        BaseAlert.__init__(self, *args, **kwargs)
        self._query_url = ''
        self._tag_keys = []
        self._group = ''
        self._default_aggregate = 'sum'

    def check(self):
        """检查非空字段"""
        pass

    @property
    def query_url(self):
        """query url 构造"""
        if not self._query_url:
            tsd_addr = self.tsd_addr
            tsd_rule = self.strategy.get('tsd_rule', {})
            metric = tsd_rule.get('metric', '')
            start, end = self.query_time()
            aggregate = self._default_aggregate
            sample = tsd_rule.get('sample', '')
            if sample:
                sample = f':0all-{sample}'
            tags = tsd_rule.get('group', [])
            if tags:
                tags_str = '{' + ','.join([f'{kv["key"]}={kv["value"]}' for kv in tags]) + '}'
            else:
                tags_str = ''
            self._query_url = f'http://{tsd_addr}/api/query?start={start}&end={end}&m={aggregate}{sample}:{metric}{tags_str}'
        return self._query_url


    def run(self):
        """
        1）通过http请求tsd拿到指标的数值
        2）对比阈值条件，得到该告警每个分组的状态信息（是否告警）、以及该告警策略的状态信息
        3）将策略及其每个分组的状态保存到redis，如果状态发送变化的，则发送通知（告警产生/撤销）
        :return:
        """
        self.check()
        task_time = self.task_time
        strategy_id = str(self.strategy['_id'])
        res = requests.get(self.query_url).json()
        LOG.debug('Request: {}, Got: {}'.format(self.query_url, res))

        group_state = {}
        flag_strategy_ok = True
        multiple_groups = True if len(res) > 1 else False
        if not res:
            # 无数据，默认为OK
            strategy_state = {
                'status': 'OK',
                'timestamp': int(task_time),
            }
        else:
            for data in res:
                # 分组信息
                group = {k: v for k, v in data['tags'].items() if k in self.groups_keys}
                group_str = ','.join([f'{k}={v}' for k, v in group.items()])
                # 分组的实际结果
                dps_values = list(data.get('dps', {}).values())
                if not dps_values:
                    continue
                else:
                    real_value = float(format(dps_values[0], '0.2f'))
                # 真实值与阈值比较
                comparison = self.strategy.get('tsd_rule', {}).get('comparison', '')
                threshold = self.strategy.get('tsd_rule', {}).get('threshold', '')
                if self.comp(real_value, comparison, threshold):
                    flag_strategy_ok = False
                    state = {'status': 'ALERT'}
                else:
                    state = {'status': 'OK'}
                # 保存该分组状态，字典序列化json
                state['timestamp'] = int(task_time)
                state['info'] = f'告警条件: {comparison} {threshold}, 检查值: {real_value}'
                group_state[group_str] = state
                LOG.debug(f'group: {group_str}, state: {state}')

            # 更新该策略的最新状态，写入redis，检查是否发送通知
            if multiple_groups:
                # 多个分组，记录OK或者Alert，以及分组keys
                strategy_state = {
                    'status': 'OK' if flag_strategy_ok else 'ALERT',
                    'timestamp': int(task_time),
                    'group_keys': list(group_state.keys())
                }
            else:
                # 只有一个分组，分组状态即告警策略的状态
                strategy_state = list(group_state.values())[0]
        LOG.debug(f'strategy({strategy_id}) status: {strategy_state}')
        r = self.redis_cli
        r.set(f'strategy:{strategy_id}:state', json.dumps(strategy_state))
        # r.zadd(f'strategy:{strategy_id}:state', strategy_state, int(task_time))
        strategy_notice = self.check_group_state(self.strategy, task_time, group_state)
        if strategy_notice:
            self.set_strategy_status(
                strategy_id=strategy_id,
                status='on' if strategy_state['status'] == 'OK' else 'alert'
            )


if __name__ == '__main__':
    pass
