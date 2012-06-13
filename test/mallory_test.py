import sys
import tornado
import tornado.gen
import tornado.httpclient
#import tornado.httpserver
import tornado.ioloop
import tornado.testing
import tornado.web

import mallory

class MalloryTest(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        app = tornado.web.Application([
            (r"/", mallory.RequestHandler)
        ])
        return app

    def get_new_ioloop(self):
        return tornado.ioloop.IOLoop.instance()

    def test_something(self):
        #self.assertEqual(1, 2)
        #http_client = tornado.httpclient.AsyncHTTPClient(io_loop = self.io_loop)
        #outbound_request = tornado.httpclient.HTTPRequest(
        #    "http://127.0.0.1:8888",
        #    method="GET"
        #)
        print self.get_url("/")
        self.http_client.fetch(self.get_url("/"), self.stop)
        response = self.wait()
        #self.assertEqual(1, 2)
        #response = yield tornado.gen.Task(http_client.fetch, outbound_request)
        print response
        self.assertEqual(1, 2)
