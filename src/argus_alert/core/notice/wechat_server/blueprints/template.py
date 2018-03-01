#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests


class Template:
    BASE_URL = 'https://api.weixin.qq.com/cgi-bin/template/'

    def __init__(self):
        pass

    def set_industry(self, access_token, id1, id2):
        url = self.BASE_URL + 'api_set_industry'
        params = {'access_token': access_token}
        data = {'industry_id1': id1, 'industry_id2': id2}
        r = requests.post(url=url, params=params, json=data)
        result = r.json()
        print(result)
        return result

    def get_my_industry(self, access_token):
        url = self.BASE_URL + 'get_industry'
        params = {'access_token': access_token}
        r = requests.get(url=url, params=params)
        result = r.json()
        print(result)
        return result

    def get_templates(self, access_token):
        url = self.BASE_URL + 'get_all_private_template'
        params = {'access_token': access_token}
        r = requests.get(url=url, params=params)
        result = r.json()
        print(result)
        return result

    def delete_template(self, access_token, template_id):
        url = self.BASE_URL + 'del_private_template'
        params = {'access_token', access_token}
        data = {'template_id': template_id}

        r = requests.post(url=url, params=params, json=data)
        result = r.json()
        print(result)
        return result

    def send_template_msg(self, access_token, data):
        url = 'https://api.weixin.qq.com/cgi-bin/message/template/send'
        params = {'access_token': access_token}

        r = requests.post(url=url, params=params, json=data)
        result = r.json()
        print(result)
        return result
