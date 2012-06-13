import tornado
import tornado.gen
import tornado.httpserver
import tornado.httpclient
import tornado.ioloop
import tornado.web
import sys
import urlparse

class RequestHandler(tornado.web.RequestHandler):

    def initialize(self, proxy_to, ca_file):
        self.proxy_to = urlparse.urlparse(proxy_to)
        self.ca_file = ca_file
        print "proxying to %s with %s" % (proxy_to, ca_file)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def handle_request(self):
        try:
            request = self._build_request()

            http_client = tornado.httpclient.AsyncHTTPClient(io_loop=tornado.ioloop.IOLoop.instance())
            response = yield tornado.gen.Task(http_client.fetch, request)

            self._send_response(response)
        except Exception as e:
            print "Unexpected error:", e

    def _build_request(self):
        uri = urlparse.urlunparse([self.proxy_to.scheme, self.proxy_to.netloc, self.request.path, None, self.request.query, None])

        headers = self.request.headers.copy()
        del headers['Host']

        if self.request.method == "GET":
            body = None
        else:
            body = self.request.body

        request = tornado.httpclient.HTTPRequest(
            uri,
            ca_certs = self.ca_file,
            method = self.request.method,
            headers = headers,
            body = body
        )
        return request

    def _send_response(self, response):
        message = response.body
        self.set_status(response.code)
        for header, value in response.headers.iteritems():
            self.set_header(header, value)
        self.write(message)
        self.finish()

    get = post = put = delete = handle_request
