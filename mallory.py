#! /usr/bin/env python

import tornado
import tornado.gen
import tornado.httpserver
import tornado.httpclient
import tornado.ioloop
import tornado.web
import sys

import mallory

app = tornado.web.Application([
    (r"/", mallory.RequestHandler)
])
http_server = tornado.httpserver.HTTPServer(app)
http_server.listen(8888)
tornado.ioloop.IOLoop.instance().start()
