#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from flask import Blueprint, g, jsonify, request

from wechat_server.blueprints import __version__
from wechat_server.blueprints.official_account import with_official_account

controller_bp = Blueprint('controller', __name__, url_prefix='/' + __version__ + '/controller')


@controller_bp.route('/create_qrcode', methods=['GET'])
@with_official_account
def create_qrcode():
    app = g.official_account
    user_id = request.args.get('username')
    expire_seconds = request.args.get('expire_seconds') or 5*60

    response = app.create_temp_qrcode(user_id, expire_seconds)
    return jsonify(response)


@controller_bp.route('/push_alert', methods=['POST'])
@with_official_account
def push_alert():
    app = g.official_account
    data = json.load(request.data.decode())

    response = app.send_template_msg(data)
    return jsonify(response)


@controller_bp.route('/delete_menus')
@with_official_account
def delete_menus():
    app = g.official_account
    response = app.delete_menus()
    return jsonify(response)


@controller_bp.route('/create_menu', methods=['POST'])
@with_official_account
def create_menu():
    app = g.official_account
    menu = json.loads(request.data.decode() or '{}')
    response = app.create_menu(menu)
    return jsonify(response)


@controller_bp.route('/query_menus')
@with_official_account
def query_menus():
    app = g.official_account
    response = app.query_menus()
    return jsonify(response)


@controller_bp.route('/current_autoreply')
@with_official_account
def current_autoreply():
    app = g.official_account
    response = app.current_autoreply_info
    return jsonify(response)
