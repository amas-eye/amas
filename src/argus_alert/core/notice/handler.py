# coding=utf-8
"""告警通知处理进程

1）监听redis队列，topic包括所有通知渠道（notice:*, *包含db/wechat/mail/api/...）
2）对应topic的告警内容，由对应的告警方式处理
"""
from queue import Queue
from threading import Thread

from redis import Redis

from argus_alert.etc.bootstrap import RunningConfig
from argus_alert.core.notice.notifier import *
from argus_alert.core.utils.log import timed_logger

LOG = timed_logger()


def run_notice_handler(*args, **kwargs):
    NoticeHandler(*args, **kwargs).run()


class NoticeHandler(object):
    """"""

    def __init__(self, mongo_addr, redis_addr, topics, workers=None):
        self._mongo_addr = mongo_addr
        self._redis_addr = redis_addr
        self._topics = topics
        self._redis_client = None
        self.q = Queue(maxsize=1)   # 监听线程和消费线程之间的队列应尽可能小，避免程序退出时仍有较多消息滞留在内存
        self.num_workers = workers if workers is not None else RunningConfig.NOTIFIER_THREADS
        self._threads = []

    @property
    def redis_client(self):
        if not self._redis_client:
            self._redis_client = Redis.from_url(self._redis_addr, decode_responses=True)
        return self._redis_client

    def boostrap_workers(self):
        """起多个线程/协程来完成通知处理工作"""

        def _worker():
            while True:
                item = self.q.get()
                ctx = {'item': item, 'mongo_addr': self._mongo_addr}
                try:
                    notify_worker(ctx).send()  
                except Exception as e:
                    LOG.error(e, exc_info=True)

        ts = [Thread(target=_worker, name=f'NoticeWorker-{n}') for n in range(self.num_workers)]
        for t in ts:
            t.start()
        self._threads.extend(ts)

    def listen_topics(self, redis_pubsub):
        """监听通知队列消息的线程"""
        def _worker():
            for item in redis_pubsub.listen():
                LOG.debug(f'Got item from pubsub: {item}')
                self.q.put(item)
        t = Thread(target=_worker, name='NoticeListener')
        t.start()
        self._threads.append(t)

    def run(self):
        pubsub = self.redis_client.pubsub(ignore_subscribe_messages=True)
        pubsub.psubscribe(self._topics)
        LOG.debug('Listening topics: {}'.format(self._topics))
        self.boostrap_workers()
        self.listen_topics(pubsub)
        for t in self._threads:
            t.join()


if __name__ == '__main__':
    nh = NoticeHandler(mongo_addr='mongodb://localhost:27017/',
                       redis_addr='redis:///@localhost:6379/0',
                       topics=['notice:*'])
    nh.run()

    # run_notice_handler('redis:///@localhost:6379/0', topics=['notice:*'])
