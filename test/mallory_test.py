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

        self.mallory_server = mallory.Server(proxy_to="https://127.0.0.1:10000", ca_file="test/ssl/server.crt", port=10001, ssl_options =  { "certfile": "test/ssl/server.crt", "keyfile": "test/ssl/server.key" })
        self.mallory_server.start()

    def tearDown(self):
        super(MalloryTest, self).tearDown()
        self.echo_http_server.stop()
        self.mallory_server.stop()

    def get_app(self):
        app = tornado.web.Application([
            (r"/", mallory.RequestHandler)
        ])
        return app

    def get_new_ioloop(self):
        return tornado.ioloop.IOLoop.instance()

    def get_url(self, path):
        return 'https://127.0.0.1:%s%s' % (10001, path)

    def test_a_200_response_on_hitting_the_root_url(self):
        self.http_client.fetch(self.get_url("/"), self.stop, ca_certs = "test/ssl/server.crt")
        response = self.wait()
        self.assertEqual(200, response.code)

    def test_path_is_proxied(self):
        self.http_client.fetch(self.get_url("/the/path/to/hit"), self.stop, ca_certs = "test/ssl/server.crt")
        response = self.wait()
        self.assertTrue(response.body.find("PATH: /the/path/to/hit") >= 0)

    def test_query_params_are_proxied(self):
        self.http_client.fetch(self.get_url("/path?param1=value1&param2=value2"), self.stop, ca_certs = "test/ssl/server.crt")
        response = self.wait()
        self.assertTrue(response.body.find("QUERY STRING: param1=value1&param2=value2") >= 0)

    def test_http_status_code_is_returned_in_the_response(self):
        self.http_client.fetch(self.get_url("/http_status/201"), self.stop, ca_certs = "test/ssl/server.crt")
        response = self.wait()
        self.assertEqual(201, response.code)

    def test_http_headers_are_passed_along(self):
        self.http_client.fetch(self.get_url("/"), self.stop, ca_certs = "test/ssl/server.crt", headers = { "X-Something": "bar" })
        response = self.wait()
        self.assertTrue(response.body.find("X-Something: bar") >= 0, response.body)

    def test_host_header_is_not_passed(self):
        self.http_client.fetch(self.get_url("/"), self.stop, ca_certs = "test/ssl/server.crt")
        response = self.wait()
        self.assertTrue(response.body.find("Host: 127.0.0.1:10000") >= 0, response.body)

    def test_response_headers_are_returned(self):
        self.http_client.fetch(self.get_url("/http_header/X-CustomHeader/header-value"), self.stop, ca_certs = "test/ssl/server.crt")
        response = self.wait()
        self.assertEqual('header-value', response.headers['X-CustomHeader'])

    def test_post_body_is_passed_along(self):
        self.http_client.fetch(self.get_url("/http_header/X-CustomHeader/header-value"), self.stop, method = "POST", body = "the post body", ca_certs = "test/ssl/server.crt")
        response = self.wait()
        self.assertTrue(response.body.find("METHOD: POST") >= 0, response.body)
        self.assertTrue(response.body.find("BODY: the post body") >= 0, response.body)

