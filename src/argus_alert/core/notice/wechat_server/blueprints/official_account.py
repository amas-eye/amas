#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Wechat Official Account server application.
"""

from urllib.parse impor urlencode
import functools
import threading
import hashlib
import json

from flask import request, g, abort
from redis import Redis

from wechat_server.blueprints.utils import (get_access_token, get_app_token,
                                            get_logger, singleton)
from wechat_server.blueprints.menu import Menu
from wechat_server.blueprints.template import Template
from wechat_server.blueprints.manager import Manager

import wechat_server.blueprints.receive as receive
import wechat_server.blueprints.reply as reply


@singleton
class OfficialAccount:
    """
    Server application holds the meta attributes and methods.
    It is server itself that should keep the access token. It's broker
    need not to hold access token, so we pass it per calling the brokers'
    methods.
    """

    def __init__(self, host='127.0.0.1', port=6379, db=0,
                 channel='wechat_binding', password=None):
        self._relationship = {}  # <ticket>: <user_id>
        self._logger = get_logger('OfficialAccountApp.log')

        self._menu = Menu()
        self._template = Template()
        self._manager = Manager()
        self._redis = Redis(host=host, port=port, db=0, password=password)
        self._redis_channel = channel

    def query_menus(self):
        result = self._menu.query(self._access_token)
        self._logger.info(f'Query menus and get {result}')
        return result

    def delete_menus(self):
        result = self._menu.delete(self._access_token)
        self._logger.warn(f'Delete menus and get {result}')
        return result

    def create_menu(self, menu):
        result = self._menu.create(self._access_token, menu)
        self._logger.warn(f'Create menus and get {result}')
        return result

    def create_temp_qrcode(self, user_id, expire_seconds):
        """Currently only support string-based `user_id ` temporary qr code."""
        _result = self._manager.create_temp_qrcode(self._access_token,
                                                   user_id, expire_seconds)
        ticket = _result.get('ticket')
        self._relationship[ticket] = user_id
        result = {'username': _result.get('user_id'),
                  'qrcode_url': _result.get('qrcode_url')}
        self._logger.warn(f'Create temporary qr code: {result}')
        return result

    def send_template_msg(self, data):
        result = self._template.send_template_msg(self._access_token, data)
        self._logger.warn(f'Send template message, {result}')
        return result

    def _request_from_wechat(self, func):
        """
        A decorator to ensure the requests will be handled are definitely
        comes from wechat.
        """

        token = get_app_token()

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            signature = request.args.get('signature')
            timestamp = request.args.get('timestamp')
            nonce = request.args.get('nonce')
            echostr = request.args.get('echostr')
            try:
                temp = ''.join(sorted([nonce, str(timestamp), token]))
                m = hashlib.sha1()
                m.update(bytes(temp, 'utf-8'))
                my_signature = m.hexdigest()
                assert signature == my_signature
            except TypeError as e:
                return abort(404)
            except AssertionError as e:
                return abort(404)
            else:
                print('Handle a request')

                if request.method == 'GET':
                    # <GET> means it's a automatic validation from wechat,
                    # we should say hi back and suspend the `func`
                    # actually we do nothing in `func`.
                    return echostr
                # Wechat POST some follower actions to use
                # let's handle it.
                return func(*args, **kwargs)
        return wrapper

    def _event_handler(self, func):
        """
        The real manager of handing request or behavior happened
        to our `OfficialAccount`.
        Currently, only support new follower from parametric QR code,
        i.e. we receive a POST request from Wechat.
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if request.method == 'GET':
                return
            try:
                xml_data = request.data.decode()
                print(f'Raw data of current receive msg: {(xml_data)}')
                rec_msg = receive.parse_xml(xml_data)
                print(f'Type of current receive msg: {type(rec_msg)}')
                # handle the new follwer from temp parametric QR code.
                if isinstance(rec_msg,
                              receive.NewFollowerFromParametricQRCodeEventMsg):
                    self._logger.info('New follower from parametric QR code.')
                    ticket = rec_msg.ticket
                    open_id = rec_msg.from_username
                    user_id = self._relationship.get(ticket)
                    push_thread = threading.Thread(target=self._push_to_redis,
                                                   args=(user_id, open_id))
                    push_thread.start()
                if isinstance(rec_msg, receive.NewTrialEventMsg):
                    BASE_URL = 'http://argus.useease.com:8383/argusphone?'
                    me = rec_msg.to_username
                    user = rec_msg.from_username
                    url = BASE_URL + urlencode({'openid': user, 'ts':
                                                int(time.time())})
                    reply_msg = reply.TrialEventMsg(user, me, url).send()
                    self._logger.info(f'New trial from wechat {url}')
                    return reply_msg
                else:
                    self._logger.info('Return the default message')
                    me = rec_msg.to_username
                    user = rec_msg.from_username
                    content = 'Hello'
                    reply_msg = reply.TextMsg(user, me, content).send()
                    return reply_msg

            except AttributeError as e:
                print(f'Missing attribute: {e}')
            # No finally clause because it defer our `return resp` in else clause
            # and execute the statements in it. A little like `defer` in golang.
        return wrapper

    @property
    def _access_token(self):
        return get_access_token()

    @property
    def current_autoreply_info(self):
        return self._manager.get_current_autoreply_info(self._access_token)

    @property
    def handlers(self):
        """
        To implement more event handler you could add some code to
        `self._event_handler` or write a brand-new decorator based instance
        method and insert it to following list

        Make sure the `self._request_from_wechat` is the last item.
        Because flask do it like this:
        @app.route('/yourpath')
        @self._request_from_wechat
        @self._event_handler
        @other_decorator
        def function(*args, *kwargs):
            pass

        Example, if your want to react to the POST request from Wechat
        whenever a follower unfollow(or unsubscribe) us you can create
        a new Class in receive.py and follow the original patter or
        create a decorator like this:

        ```
        def _handle_unfollow(self, func):
            def wrapper(*args, **kwargs):
                if request.method == 'GET':
                    abort(404)
                xml_data = request.data.decode()
                # then do something
                # like unbind their openid to the id of your system.
                # notify something or somebody
            return wrapper
        ````
        Then change the return value of `handers' to
        return [self.handle_unfollow, self._request_from_wechat]

        Add your code in `self._event_handler(self, func)`(former appoach) is
        appreciated, because the data POST from Wechat just differ in a little
        fields, retreive it once and new a instance is more memory-effective.
        """

        return [self._event_handler, self._request_from_wechat]

    def _push_to_redis(self, user_id, open_id):
        self._logger.info(f'Push {user_id}: {open_id} into redis')
        result = {'username': user_id,
                  'open_id': open_id}
        self._redis.publish(self._redis_channel, json.dumps(result))


def with_official_account(func):
    """
    Make sure the initial arguments are the same.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            g.official_account
        except AttributeError as e:
            # A new instance which seems to be cause a overflow of
            # wechat accesstoken, but it's from another decorator,
            # so nothing is serious.
            g.official_account = OfficialAccount()
        return func(*args, **kwargs)
    return wrapper
