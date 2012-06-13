import mallory.py

import sys
import tornado
import tornado.gen
import tornado.httpclient
#import tornado.httpserver
import tornado.ioloop
import tornado.testing
import tornado.web

class MalloryTest(tornado.testing.AsyncTestCase):
    @tornado.gen.engine
    def test_something(self):
        #self.assertEqual(1, 2)
        http_client = tornado.httpclient.AsyncHTTPClient(io_loop = self.io_loop)
        outbound_request = tornado.httpclient.HTTPRequest(
            "http://127.0.0.1:8888",
            method="GET"
        )
        http_client.fetch(outbound_request, self.stop)
        response = self.wait()
        #self.assertEqual(1, 2)
        #response = yield tornado.gen.Task(http_client.fetch, outbound_request)
        print response
        self.assertEqual(1, 2)
