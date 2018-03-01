#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Handler for interface defined in
https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1443433542.
"""

from urllib.parse import urlencode
import requests


class Manager:
    PARAMETRIC_QRCODE_URL = 'https://api.weixin.qq.com/cgi-bin/qrcode/create'
    CURRENT_AUTOREPLY_INFO = 'https://api.weixin.qq.com/cgi-bin/get_current_autoreply_info'

    def __init__(self):
        pass

    def create_temp_qrcode(self, access_token, user_id, expire_seconds):
        """Currently only support string-based `user_id ` temporary qr code."""

        data = {
            "expire_seconds": expire_seconds,
            "action_name": "QR_STR_SCENE",
            "action_info": {
                "scene": {
                    "scene_str": user_id
                }
            }
        }

        url = 'https://api.weixin.qq.com/cgi-bin/qrcode/create'
        params = {'access_token': access_token}
        r = requests.post(url=url, params=params, json=data)

        result = r.json()
        print(f'A temporary QR code just created for {user_id}:\n {result}')
        ticket = result.get('ticket')
        if ticket:
            qr_url = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?' + urlencode({'ticket': ticket})
        else:
            qr_url = None

        return {'user_id': user_id, 'qrcode_url': qr_url, 'ticket': ticket}

    def get_current_autoreply_info(self, access_token):
        url = self.CURRENT_AUTOREPLY_INFO
        params = {'access_token': access_token}
        r = requests.get(url=url, params=params)

        result = r.json()
        return result
