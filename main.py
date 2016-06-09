__author__ = 'zhangxa'

from OpenSpider.SpiderCelery.celery import app
from OpenSpider.SpiderCelery import tasks
from tornado.ioloop import IOLoop
from tornado import gen,queues

import time
import tcelery

tcelery.setup_nonblocking_producer()

base_url = 'http://www.jianshu.com'
concurrency = 5

@gen.coroutine
def main():
    yield gen.sleep(3)

    q = queues.Queue()
    fetching,fetched = set(),set()

    @gen.coroutine
    def fetch_url():
        cur_url = yield q.get()
        try:
            if cur_url in fetching:
                return

            print("fetching url:%s" % cur_url)
            fetching.add(cur_url)
            urls = yield gen.Task(tasks.jianshu_crawler.apply_async,args=[cur_url])
            fetched.add(cur_url)
            url_lists = urls.result
            if not url_lists:
                return
            for url in url_lists:
                yield q.put(url)
        finally:
            q.task_done()

    @gen.coroutine
    def worker():
        while True:
            yield fetch_url()

    q.put(base_url)

    for _ in range(concurrency):
        worker()

    yield q.join()

if __name__ == "__main__":
    IOLoop.current().run_sync(main)