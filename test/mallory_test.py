import sys
import tornado
import tornado.gen
import tornado.httpclient
import tornado.httpserver
import tornado.ioloop
import tornado.testing
import tornado.web

import mallory
import test

class MalloryTest(tornado.testing.AsyncHTTPTestCase):
    def setUp(self):
        super(MalloryTest, self).setUp()

        echo_app = tornado.web.Application([
            (r"/", test.EchoRequestHandler)
        ])
        self.echo_http_server = tornado.httpserver.HTTPServer(echo_app, io_loop=self.io_loop, **self.get_httpserver_options())
        self.echo_http_server.listen(tornado.testing.get_unused_port(), address="127.0.0.1")


    def tearDown(self):
        super(MalloryTest, self).tearDown()
        self.echo_http_server.stop()

    def get_app(self):
        app = tornado.web.Application([
            (r"/", mallory.RequestHandler)
        ])
        return app

    def get_httpserver_options(self):
        #return { "ssl_options":  { "certfile": "test/ssl/server.crt", "keyfile": "test/ssl/server.key" } }
        return {}

    def get_new_ioloop(self):
        return tornado.ioloop.IOLoop.instance()

    def get_url(self, path):
        """Returns an absolute url for the given path on the test server."""
        #return 'https://localhost:%s%s' % (self.get_http_port(), path)
        return 'http://localhost:%s%s' % (10001, path)

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
        print response.body
        self.assertEqual(1, 2)
