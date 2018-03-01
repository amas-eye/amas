# coding=utf-8
"""实现发送slack通知的公共方法
"""
from requests import post


def send_slack_via_hook(hook_url, text, *args, **kwargs):
    """"""
    post(url=hook_url, json={'text': text})