#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask

from blueprints.wechat_alert_push_bp import alert_bp
from blueprints.wechat_app_controller_bp import controller_bp

app = Flask(__name__)

app.register_blueprint(alert_bp)
app.register_blueprint(controller_bp)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
