import datetime
import socket
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

class CircuitBreakerTest(tornado.testing.AsyncTestCase):
    def setUp(self):
        super(CircuitBreakerTest, self).setUp()
        self.client = test.MalloryClient(10002, self)

        echo_app = tornado.web.Application([
            (r"/.*", test.EchoRequestHandler)
        ])
        self.echo_http_server = tornado.httpserver.HTTPServer(
         echo_app,
         ssl_options = {
             "certfile": "test/ssl/echo_server/server.crt",
             "keyfile": "test/ssl/echo_server/server.key",
         }
        )

        http_request_options = {
            "ca_certs": "test/ssl/ca/ca.crt",
            "request_timeout": 0.5
        }
        ssl_options = {
            "certfile": "test/ssl/mallory/server.crt",
            "keyfile": "test/ssl/mallory/server.key"
        }
        self.mallory_server = mallory.Server(proxy_to="https://127.0.0.1:10000", port=10002, http_request_options=http_request_options, ssl_options=ssl_options)
        self.mallory_server.start()

    def tearDown(self):
        super(CircuitBreakerTest, self).tearDown()
        self.echo_http_server.stop()
        self.mallory_server.stop()

    def get_url(self, path):
        return 'https://127.0.0.1:%s%s' % (10002, path)

    def get_new_ioloop(self):
        return tornado.ioloop.IOLoop.instance()

    def test_circuit_breaker_starts_open(self):
        response = self.client.get("/_mallory/heartbeat", self)

        self.assertEqual(200, response.code)

    def test_circuit_breaker_trips_when_you_cant_connect_to_proxy_three_times_in_a_row(self):
        self.client.get("/", self)
        response = self.client.get("/_mallory/heartbeat", self)
        self.assertEqual(200, response.code)

        self.client.get("/", self)
        self.client.get("/", self)

        response = self.client.get("/_mallory/heartbeat", self)
        self.assertEqual(503, response.code)

    def test_circuit_breaker_resets_if_a_request_succeeds(self):
        self.client.get("/", self)
        self.client.get("/", self)
        self.client.get("/", self)

        response = self.client.get("/_mallory/heartbeat", self)
        self.assertEqual(503, response.code)

        self.echo_http_server.listen(10000, address="127.0.0.1")

        self.client.get("/", self)
        response = self.client.get("/_mallory/heartbeat", self)
        self.assertEqual(200, response.code)

    def test_circuit_breaker_resets_when_it_can_make_a_tcp_connection_to_the_target(self):
        self.client.get("/", self)
        self.client.get("/", self)
        self.client.get("/", self)

        response = self.client.get("/_mallory/heartbeat", self)
        self.assertEqual(503, response.code)

        self.echo_http_server.listen(10000, address="127.0.0.1")

        def assert_circuit_breaker_reset():
            response = self.client.get("/_mallory/heartbeat", self)
            self.assertEqual(200, response.code)
            self.stop()

        tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(milliseconds=1250), assert_circuit_breaker_reset)
        self.wait()

    def test_port_defaults_to_80_for_http_urls(self):
        circuit_breaker = mallory.CircuitBreaker("http://example.com")
        self.assertEqual(80, circuit_breaker.port)

    def test_port_defaults_to_443_for_https_urls(self):
        circuit_breaker = mallory.CircuitBreaker("https://example.com")
        self.assertEqual(443, circuit_breaker.port)

    def test_port_is_extracted_from_url_if_specified(self):
        circuit_breaker = mallory.CircuitBreaker("https://example.com:8192")
        self.assertEqual(8192, circuit_breaker.port)


