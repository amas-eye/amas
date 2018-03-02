#!/usr/bin/env python3
# coding=utf-8
"""强制终止进程
"""
import sys, os
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(base_dir))

from argus_alert.core.utils.common import kill_all

# TODO
kill_all()

