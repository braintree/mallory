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
            (r"/.*", test.EchoRequestHandler)
        ])
        self.echo_http_server = tornado.httpserver.HTTPServer(echo_app, ssl_options =  { "certfile": "test/ssl/server.crt", "keyfile": "test/ssl/server.key" })
        self.echo_http_server.listen(10000, address="127.0.0.1")

        mallory_app = tornado.web.Application([
            (r"/.*", mallory.RequestHandler, dict(proxy_to = "https://127.0.0.1:10000", ca_file = "test/ssl/server.crt"))
        ])
        self.mallory_http_server = tornado.httpserver.HTTPServer(mallory_app, ssl_options =  { "certfile": "test/ssl/server.crt", "keyfile": "test/ssl/server.key" })
        self.mallory_http_server.listen(10001, address="127.0.0.1")

    def tearDown(self):
        super(MalloryTest, self).tearDown()
        self.echo_http_server.stop()
        self.mallory_http_server.stop()

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

    def test_a_200_response_on_hitting_the_root_url(self):
        self.http_client.fetch(self.get_url("/"), self.stop, ca_certs = "test/ssl/server.crt")
        response = self.wait()
        self.assertEqual(200, response.code)

    def test_path_is_proxied(self):
        self.http_client.fetch(self.get_url("/the/path/to/hit"), self.stop, ca_certs = "test/ssl/server.crt")
        response = self.wait()
        print response.body
        self.assertTrue(response.body.find("PATH: /the/path/to/hit") >= 0)
