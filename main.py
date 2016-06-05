__author__ = 'zhangxa'

from SpiderCelery.celery import app
from SpiderCelery import tasks
from tornado.ioloop import IOLoop
from tornado import gen,queues

import time
import tcelery

tcelery.setup_nonblocking_producer()

base_url = 'http://www.hao123.com'
concurrency = 20

@gen.coroutine
def main():
    yield gen.sleep(1)

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
            urls = yield gen.Task(tasks.fetch_a_url.apply_async,args=[cur_url])
            fetched.add(cur_url)
            for url in urls.result:
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