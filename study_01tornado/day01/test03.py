#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# @Time    : 2017/8/13 19:00
# @Author  : goustzhu <goustzhu@gmail.com>
# @File    : test03.py
import sys, os, time, datetime

#!/bin/env python

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import tornado.gen
from tornado.concurrent import run_on_executor
# 这个并发库在python3自带在python2需要安装sudo pip install futures
from concurrent.futures import ThreadPoolExecutor

import time

from tornado.options import define, options
define("port", default=8100, help="run on the given port", type=int)

class SleepHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(2)
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        # 假如你执行的异步会返回值被继续调用可以这样(只是为了演示),否则直接yield就行
        # res = yield self.sleep()
        self.sleep()
        self.write("when i sleep")
        self.finish()

    @run_on_executor
    def sleep(self):
        time.sleep(5)
        print 'ffffffffff'
        return 5

class JustNowHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("i hope just now see you")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[
            (r"/sleep", SleepHandler), (r"/justnow", JustNowHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
