#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
I was trying to decouple web framework the one provide us capability of
handling http request, specifically, in `flask`, we could manipulate urls via
coding view functions and the Wechat Official Account application logic which
allow us interact with followers by handle some http requests too. Turns out,
there is not neccessary to decouple them, aka, they are related. Here i use
flask's elegant class-based view function as our broker of accepting http
requests and returning response. All the wechat logic is stashed with the help
of Python decorators.
"""

from flask import Blueprint
from flask.views import MethodView

from wechat_server.blueprints import __version__
from wechat_server.blueprints.official_account import OfficialAccount

__all__ = ['alert_bp']

wechat_app = OfficialAccount()

alert_bp = Blueprint('alert', __name__, url_prefix='/' + __version__ + '/wechat_alert')


class WechatAlertAPI(MethodView):
    """
    A class-based http method handler.
    All the business logic is handle by the decorators.
    To add functionalities, implement them and append them to `decorators`.
    """

    decorators = wechat_app.handlers

    def get(self):
        """Wechat will visit us via GET to ensure secure communication."""
        pass

    def post(self):
        """
        Whenever the followers make some actions, Wechat will post some
        data to us and hope us react to followers' behavior via POST
        something back to it.
        """
        pass


alert_bp.add_url_rule('/', view_func=WechatAlertAPI.as_view('alert_view'))
