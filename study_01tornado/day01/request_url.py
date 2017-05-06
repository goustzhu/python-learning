#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# @Time    : 2017/3/19 10:53
# @Author  : goustzhu <goustzhu@gmail.com>
# @File    : request_url.py
import sys, os, time, datetime

reload(sys)
sys.setdefaultencoding('utf-8')
#!/usr/bin/env python
#coding:utf-8

import textwrap

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="Please send email to me", type=int)

class ReverseHandler(tornado.web.RequestHandler):
    def get(self, input_word):
        self.write(input_word[::-1])

class WrapHandler(tornado.web.RequestHandler):
    def post(self):
        text = self.get_argument("text")
        width = int(self.get_argument("width", 40))
        print type(text), type(width)
        self.write(textwrap.fill(text, width))

def start_up():
    app = tornado.web.Application(
        handlers=[
            (r"/reverse/(\w+)", ReverseHandler),
            (r"/wrap", WrapHandler)
        ]
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    tornado.options.parse_command_line()
    start_up()
    # app = tornado.web.Application(
    #     handlers=[
    #         (r"/reverse/(\w+)", ReverseHandler),
    #         (r"/wrap", WrapHandler)
    #     ]
    # )
    # http_server = tornado.httpserver.HTTPServer(app)
    # http_server.listen(options.port)
    # tornado.ioloop.IOLoop.instance().start()