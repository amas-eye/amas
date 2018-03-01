#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Handler for interface defined in
https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421141013.

This file is to set up customized menu in your official account.
And react to user behaviors.
"""

import os

import requests


class Menu:
    BASE_URL = 'https://api.weixin.qq.com/cgi-bin/menu/'
    DEFAULT_MENU = {
        'button': [
            {
                'name': 'Argus',
                'type': 'view',
                'url': os.environ.get('MOBILE_PAGE') or 'http://127.0.0.1/some_pth'
            },
            {
                'name': 'Useease',
                'type': 'view',
                'url': 'http://www.useease.com'
            },
            {
                'name': 'Have a try',
                'type': 'click',
                'key': 'trial_argus'
            }
        ]
    }

    def __init__(self):
        pass

    def create(self, access_token, menu: dict = None):
        """
        Create a customized menu according to `menu`.
        If `menu` is None, will creat a default menu.
        """
        url = self.BASE_URL + 'create'
        params = {'access_token': access_token}
        if not menu:
            data = self.DEFAULT_MENU
        else:
            data = menu
        r = requests.post(url=url, params=params, json=data)
        result = r.json()
        print(result)
        return result

    def query(self, access_token):
        url = self.BASE_URL + 'get'
        params = {'access_token': access_token}
        r = requests.get(url=url, params=params)
        result = r.json()
        print(result)
        return result

    def delete(self, access_token):
        """All memus will be permanently deleted."""

        url = self.BASE_URL + 'delete'
        params = {'access_token': access_token}
        r = requests.get(url=url, params=params)
        result = r.json()
        print(result)
        return result

    def get_current_menus_conf(self, access_token):
        """
        Details in:
        https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1434698695
        """

        url = "https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info"
        params = {'access_token': access_token}
        r = requests.get(url=url, params=params)
        result = r.json()
        print(result)
        return result
