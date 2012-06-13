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
    def get(self):
        try:
            uri = urlparse.urlunparse([self.proxy_to.scheme, self.proxy_to.netloc, self.request.path, None, self.request.query, None])
            passed_headers = self.request.headers.copy()
            del passed_headers['Host']
            outbound_request = tornado.httpclient.HTTPRequest(
                uri,
                ca_certs = self.ca_file,
                method = "GET",
                headers = passed_headers
            )
            http_client = tornado.httpclient.AsyncHTTPClient(io_loop=tornado.ioloop.IOLoop.instance())

            response = yield tornado.gen.Task(http_client.fetch, outbound_request)

            message = response.body
            self.set_status(response.code)
            self.set_header('Content-Length', len(message))
            for header, value in response.headers.iteritems():
                self.set_header(header, value)

            self.write(message)
            self.finish()

        except Exception as e:
            print "Unexpected error:", e

