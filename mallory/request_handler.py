import logging
import socket
import tornado
import tornado.gen
import tornado.httpserver
import tornado.httpclient
import tornado.ioloop
import tornado.web
import sys
import urlparse

class RequestHandler(tornado.web.RequestHandler):

    def initialize(self, circuit_breaker, proxy_to, http_request_options):
        self.circuit_breaker = circuit_breaker
        self.proxy_to = urlparse.urlparse(proxy_to)
        self.http_request_options = http_request_options

    @tornado.web.asynchronous
    @tornado.gen.engine
    def handle_request(self):
        try:
            request_id = self._request_id()
            logging.info("request %s proxying to %s%s" % (request_id, self.proxy_to.netloc, self.request.path))

            request = self._build_request()

            http_client = tornado.httpclient.AsyncHTTPClient(io_loop=tornado.ioloop.IOLoop.instance())
            response = yield tornado.gen.Task(http_client.fetch, request)
            if response.code == 599:
                logging.warn("request %s failed with %s" % (request_id, response.error))
                self.circuit_breaker.report_error()
                self._send_error_response()
            else:
                logging.info("request %s succeeded with %s" % (request_id, response.code))
                self.circuit_breaker.report_success()
                self._send_response(response)
        except Exception as e:
            logging.exception("Unexpected error: %s" % str(e))
            self._send_error_response()

    def _build_request(self):
        uri = urlparse.urlunparse([self.proxy_to.scheme, self.proxy_to.netloc, self.request.path, None, self.request.query, None])

        headers = self.request.headers.copy()
        del headers['Host']

        if self.request.method in ["DELETE", "GET", "HEAD"]:
            body = None
        else:
            body = self.request.body

        request = tornado.httpclient.HTTPRequest(
            uri,
            method = self.request.method,
            headers = headers,
            body = body,
            **self.http_request_options
        )
        return request

    def _request_id(self):
        if 'X-Request-Id' in self.request.headers:
            return self.request.headers['X-Request-Id']
        else:
            return '-'

    def _request_summary(self):
        return "request %s %s %s (%s)" % (self._request_id(), self.request.method,  self.request.path, self.request.remote_ip)

    def _send_error_response(self):
        self.set_status(502)
        self.set_header("X-Proxy-Server", socket.gethostname())
        self.finish()

    def _send_response(self, response):
        message = response.body
        self.set_status(response.code)
        headers = response.headers.copy()
        if 'Transfer-Encoding' in headers:
            del headers['Transfer-Encoding']
        if 'Content-Encoding' in headers:
            del headers['Content-Encoding']

        for header, value in headers.iteritems():
            self.set_header(header, value)
        self.set_header("X-Proxy-Server", socket.gethostname())
        self.set_header("Content-Length", len(message))
        self.write(message)
        self.finish()

    get = post = put = delete = head = handle_request
