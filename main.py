__author__ = 'zhangxa'

from OpenSpider.SpiderCelery.celery import app
from OpenSpider.SpiderCelery import tasks
from OpenSpider.spiderQueue.driver import QueueDriverManage
from tornado.ioloop import IOLoop
from tornado import gen,queues

import time
import tcelery

tcelery.setup_nonblocking_producer()

base_url = 'http://www.jianshu.com'
concurrency = 10

@gen.coroutine
def main():
    yield gen.sleep(3)
    settings = {"driver":"redis","driver_settings":{
            "host": "localhost",
                "port": 6379,
                "db": 1
        }}
    manger = QueueDriverManage(**settings)
    q = manger.get_queue_driver()


    @gen.coroutine
    def fetch_url():
        cur_url = yield q.get()
        try:
            print("fetching url:%s" % cur_url)
            urls = yield gen.Task(tasks.jianshu_crawler.apply_async,args=[cur_url])
            url_lists = urls.result
            if not url_lists:
                return
            for url in url_lists:
                yield q.put(url)
        except Exception as e:
            print("a exception:",e)

    @gen.coroutine
    def worker():
        while True:
            yield fetch_url()

    q.put(base_url)

    for _ in range(concurrency):
        worker()

    yield q.join(None)

if __name__ == "__main__":
    IOLoop.current().run_sync(main)