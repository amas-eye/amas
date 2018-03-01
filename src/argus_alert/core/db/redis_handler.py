# coding=utf-8
"""redis客户端连接维护
"""
from redis import Redis


class RedisClient(object):
    def __init__(self, url=None, host='localhost', port=6379, **kwargs):
        self._url = url
        self._host = host
        self._port = port
        self._client = None
        self._kwargs = kwargs

    @property
    def client(self):
        if self._client is None:
            if self._url is not None:
                self._client = Redis.from_url(self._url)
            else:
                self._client = Redis(host=self._host, port=self._port, **self._kwargs)
        return self._client


if __name__ == '__main__':
    rc = RedisClient('redis:///@localhost:6379/0').client
    print(rc.hgetall('config:test'))
