#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Some unit test involve request context in flask, i am not familiar to
it now, so may test without the request, but the damn logic and function-
alities are here.
"""

import unittest

import requests

from wechat_server.blueprints.receive import (parse_xml, Msg,)
from wechat_server.blueprints.utils import *
from wechat_server.blueprints.template import *
from wechat_server.blueprints.follower import *
from wechat_server.blueprints.official_account import OfficialAccount


class TestReceive(unittest.TestCase):
    @unittest.skip('Passed')
    def test_parse_xml(self):
        raw = '''
        <xml><ToUserName><![CDATA[gh_da923906810d]]></ToUserName>
        <FromUserName><![CDATA[o7EiAw9e-p86l_DL8Eb2OF32-o7g]]></FromUserName>
        <CreateTime>1511326608</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[bb]]></Content>
        <MsgId>6491098355419280763</MsgId>
        </xml>
        '''
        obj = parse_xml(raw)
        self.assertIsInstance(obj, Msg)

    @unittest.skip('Need to fix bug')
    def test_upload_temp_media(self):
        path = '/home/gouhao/thrift/README.md'
        result = upload_temp_media(path, 'text')
        self.assertIsInstance(result, dict)

    @unittest.skip('Already setted')
    def test_set_industry(self):
        result = set_industry(2, 5)
        self.assertIsInstance(result, dict)

    @unittest.skip('Passed')
    def test_get_my_industry(self):
        result = get_my_industry()
        self.assertIsInstance(result, dict)

    @unittest.skip('Passed')
    def test_get_my_template_industry(self):
        result = get_all_private_template()
        self.assertIsInstance(result, dict)

    @unittest.skip('Passed')
    def test_delete_template(self):
        result = delete_template('_agkfvXtzEDwraVGzOgyQNeSjmEeh_uRPiLeMKNNEhk')
        self.assertIsInstance(result, dict)

    @unittest.skip('Passed')
    def test_send_template_msg(self):
        data = {
                'touser':'o7EiAw9e-p86l_DL8Eb2OF32-o7g',
                'template_id': 'LWnyoj9jR4HRB7N-JCxFmJHE-Pv0Dpevoqn44kFRgeg',
                'data': {
                    'metric': {
                        'value':'cluster.cpu.usage',
                        'color': '#FF0000'
                    },
                    'host': {
                        'value':'cdh180',
                        'color': '#FF0000'
                    },
                    'solution': {
                        'value':'reboot',
                    },
                    'manager': {
                        'value':'xiaowen',
                    }
            }
        }
        result = requests.post(url='http://104.224.138.236:80/controller/push_alert/', json=data)

        self.assertIsInstance(result, dict)

    @unittest.skip('Passed')
    def test_get_followers(self):
        result = get_followers()
        self.assertIsInstance(result, dict)

    @unittest.skip('Passed')
    def test_get_follower_info(self):
        followers = {
            'openid': 'o7EiAw7fnIo1lcHtGe7K8z1FHPYc',
            'lang': 'zh_CN'
        }
        result = get_follower_info(followers)
        self.assertIsInstance(result, dict)

    @unittest.skip('Passed')
    def test_create_temp_qrcode(self):
        print('testing create qr code.')
        account = OfficialAccount()
        data = {
            'expire_seconds': 3600,
            'action_name': 'QR_STR_SCENE',
            'action_info': {
                'scene': {
                    'scene_str': 'for user1'
                }
            }
        }
        result = account.create_temp_qrcode(data, 'user1')
        self.assertIsInstance(result, dict)


if __name__ == '__main__':
    unittest.main()
