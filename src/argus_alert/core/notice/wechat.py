# coding=utf-8
"""实现发送微信通知的公共方法
"""

import os
import asyncio

from pymongo import MongoClient
import aiohttp


PUSH_ALERT_URL = os.environ.get('PUSH_ALERT_URL') or 'http://127.0.0.1/some_path'


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

    assert tasks is not None, '`tasks` should be not none iterable.'

    user_ids = [task.get('username') for task in tasks]
    user_id2open_id = {}

    client = get_client()
    db = client['argus_users']
    coll = db['users']
    for user_id in user_ids:
        condition = {'wechat_id': user_id}
        cursor = coll.find(condition)
        for user in cursor:
            user_id2open_id[user_id] = user['wechat_id']
    client.close()

    pushes = []
    for task in tasks:
        push = {}  # Conform the wechat pattern
        push['template_id'] = task.get('template_id')
        push['data'] = task.get('data')
        push['touser'] = user_id2open_id.get(task.get('username'))
        pushes.append(push)

    # Should use `asyncio.new_event_loop()` instead in non-main thread.
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    event_loop.run_until_complete(_async_send_wechat(pushes))
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
                print(resp.status)
                print(await resp.text())
