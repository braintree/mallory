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

class MalloryTest(tornado.testing.AsyncTestCase):
    def setUp(self):
        super(MalloryTest, self).setUp()
        self.http_client = tornado.httpclient.AsyncHTTPClient()

        echo_app = tornado.web.Application([
            (r"/", test.EchoRequestHandler)
        ])
        self.echo_http_server = tornado.httpserver.HTTPServer(echo_app)
        self.echo_http_server.listen(10000, address="127.0.0.1")

        mallory_app = tornado.web.Application([
            (r"/", mallory.RequestHandler)
        ])
        self.mallory_http_server = tornado.httpserver.HTTPServer(mallory_app, ssl_options =  { "certfile": "test/ssl/server.crt", "keyfile": "test/ssl/server.key" })
        self.mallory_http_server.listen(10001, address="127.0.0.1")

    def tearDown(self):
        super(MalloryTest, self).tearDown()
        self.echo_http_server.stop()

    def get_app(self):
        app = tornado.web.Application([
            (r"/", mallory.RequestHandler)
        ])
        return app

    def get_new_ioloop(self):
        return tornado.ioloop.IOLoop.instance()

    def get_url(self, path):
        """Returns an absolute url for the given path on the test server."""
        return 'https://127.0.0.1:%s%s' % (10001, path)

    def test_something(self):
        #self.assertEqual(1, 2)
        #http_client = tornado.httpclient.AsyncHTTPClient(io_loop = self.io_loop)
        #outbound_request = tornado.httpclient.HTTPRequest(
        #    "http://127.0.0.1:8888",
        #    method="GET"
        #)
        print self.get_url("/")
        self.http_client.fetch(self.get_url("/"), self.stop, ca_certs = "test/ssl/server.crt")
        response = self.wait()
        #self.assertEqual(1, 2)
        #response = yield tornado.gen.Task(http_client.fetch, outbound_request)
        print response
        print response.body
        self.assertEqual(1, 2)
