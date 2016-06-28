__author__ = 'zhangxa'

import unittest

from OpenSpider.spiderQueue.driver import QueueDriverFactory,QueueDriverManage
from OpenSpider.spiderQueue.redisqueue import RedisQueue

class QueueDriverFactory_test(unittest.TestCase):
    def test_Driver_Create_Redis(self):
        cls = QueueDriverFactory.create_queue("redis")
        self.assertIs(cls,RedisQueue)

class QueueDriverMangager_test(unittest.TestCase):
    def test_Driver_Manger(self):
        settings = {"driver":"redis","driver_settings":{
            "host": "localhost",
                "port": 6379,
                "db": 1
        }}
        manger = QueueDriverManage(**settings)
        driver = manger.get_queue_driver()
        self.assertIsInstance(driver,RedisQueue)

if __name__ == "__main__":
    unittest.main(warnings="ignore")