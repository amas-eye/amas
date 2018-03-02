# coding=utf-8
"""实现发送微信通知的公共方法
"""

import os
import asyncio

from pymongo import MongoClient
import aiohttp
from argus_alert.core.utils.log import timed_logger
from argus_alert.etc.bootstrap import DefaultConfig

LOG = timed_logger()
# PUSH_ALERT_URL = os.environ.get('PUSH_ALERT_URL') or 'http://127.0.0.1/some_path'
# PUSH_ALERT_URL = "http://114.215.85.142/argus-internal/controller/push_alert"
PUSH_ALERT_URL = DefaultConfig.PUSH_ALERT_URL

def send_wechat(tasks: list):
    """
    Push the template message to specific user.

    :param `tasks`: A iterable container of `dict` which has at
                    least 2 fields: <username>, <data>.
                    Example `tasks`:
                    [
                        {
                            'username': 'unique identifier in our system',
                            #'template_id': optional ?? considering
                            'data': {
                                'key1': value1,
                                'key2': value2,
                            },
                        },
                        #other push units
                    ]

    """

    r"""
    Actually the following json is gonna to be posted to official account.
    data = {
        'touser':'o7EiAw9e-p86l_DL8Eb2OF32-o7g',
        'template_id': 'LWnyoj9jR4HRB7N-JCxFmJHE-Pv0Dpevoqn44kFRgeg',
        'data': {
            'key1': {
                'value':'cluster.cpu.usage',
                'color': '#FF0000'
            },
            'key2': {
                'value':'cdh180',
                'color': '#FF0000'
            },
            'key3': {
                'value':'reboot',
            },  # and so on
        }
    }
    """
    
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    event_loop.run_until_complete(_async_send_wechat(tasks))
    event_loop.close()


def get_client():
    try:
        client = MongoClient(host='192.168.0.253', port=27017)
    except Exception:
        raise
    else:
        return client


async def _async_send_wechat(pushes):
    async with aiohttp.ClientSession() as session:
        for push in pushes:
            async with session.post(url=PUSH_ALERT_URL, json=push) as resp:
                # print(resp.status)
                LOG.debug(f'wechat push return status {resp.status}')
                # print(await resp.text())
                resp_text = await resp.text()
                LOG.debug(f'wechat push return status {resp_text}')
                LOG.debug('POST wechat +1')
        LOG.debug('wechat_pushes done')