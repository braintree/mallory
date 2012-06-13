import tornado
import tornado.gen
import tornado.httpserver
import tornado.httpclient
import tornado.ioloop
import tornado.web
import sys

class RequestHandler(tornado.web.RequestHandler):

    def initialize(self, proxy_to = None):
        self.proxy_to = proxy_to
        print "proxying to %s" % proxy_to

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        try:
            print "proxying to %s" % self.proxy_to
            outbound_request = tornado.httpclient.HTTPRequest(
                self.proxy_to,
                method="GET"
            )
            http_client = tornado.httpclient.AsyncHTTPClient(io_loop=tornado.ioloop.IOLoop.instance())
            #print "yielding"
            response = yield tornado.gen.Task(http_client.fetch, outbound_request)
            print response

            message = "You requested %s\n" % "hi"
            self.write("HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n%s" % (len(message), message))
            self.finish()

        except Exception as e:
            print "Unexpected error:", e

