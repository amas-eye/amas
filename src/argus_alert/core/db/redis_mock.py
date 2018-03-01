# coding=utf-8
"""
"""
from collections import deque


class FakeRedis(object):
    """类Redis API接口的内存数据库，可作为自带的nosql、或者开发测试用途"""
    def __init__(self):
        self._lists = {}
        self._dict = {}
        self._set = set()

    def get_list(self, list_name):
        if list_name not in self._lists:
            self._lists[list_name] = deque()
        return self._lists.get(list_name)

    def rpush(self, list_name, item):
        self.get_list(list_name).append(item)

    def lpush(self, list_name, item):
        self.get_list(list_name).appendleft(item)

    def lpop(self, list_name):
        return self.get_list(list_name).popleft()

    def rpop(self, list_name):
        return self.get_list(list_name).pop()


def main():
    """"""


if __name__ == '__main__':
    main()