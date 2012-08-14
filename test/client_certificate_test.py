import ssl
import tornado.httpserver
import tornado.ioloop
import tornado.testing

import mallory
import test

class ClientCertificateTest(tornado.testing.AsyncTestCase):
    def setUp(self):
        super(ClientCertificateTest, self).setUp()

        self.client = test.MalloryClient(11001, self)

        echo_app = tornado.web.Application([
            (r"/.*", test.EchoRequestHandler)
        ])
        self.echo_http_server = tornado.httpserver.HTTPServer(
         echo_app,
         ssl_options = {
            "cert_reqs": ssl.CERT_REQUIRED,
            "ca_certs": "test/ssl/ca/ca.crt",
            "certfile": "test/ssl/echo_server/server.crt",
            "keyfile": "test/ssl/echo_server/server.key",
         }
        )
        self.echo_http_server.listen(11000, address="127.0.0.1")

        http_request_options = {
            "client_key": "test/ssl/client/client.key",
            "client_cert": "test/ssl/client/client.crt",
            "ca_certs": "test/ssl/ca/ca.crt",
            "request_timeout": 0.5
        }

        ssl_options = {
            "certfile": "test/ssl/mallory/server.crt",
            "keyfile": "test/ssl/mallory/server.key"
        }

        self.mallory_server = mallory.Server(proxy_to="https://127.0.0.1:11000", http_request_options=http_request_options, port=11001, ssl_options=ssl_options)

        self.mallory_server.start()

    def tearDown(self):
        super(ClientCertificateTest, self).tearDown()
        self.echo_http_server.stop()
        self.mallory_server.stop()

    def get_new_ioloop(self):
        return tornado.ioloop.IOLoop.instance()


    def test_client_certificate(self):
        response = self.client.get("/", self)
        self.assertEqual(200, response.code)

