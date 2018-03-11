# coding=utf-8
"""测试common.py的公共方法
"""
from unittest import TestCase
from argus_collector.collectors.common import *


class CommonTest(TestCase):
    """"""
    def setUp(self):
        """"""

    def tearDown(self):
        """"""

    def test_cache(self):
        """测试缓存装饰器"""
        @cache
        def foo(n):
            return range(n)

        assert foo(2) == [0, 1]
        assert id(foo(3)) == id(foo(3)), 'id should be equal!'
