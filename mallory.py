#! /usr/bin/env python

import tornado
import tornado.gen
import tornado.httpserver
import tornado.httpclient
import tornado.ioloop
import tornado.web
import sys


class AwesomeHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(request):
        try:
            outbound_request = tornado.httpclient.HTTPRequest(
                "https://pgrs.net",
                method="GET"
            )
            http_client = tornado.httpclient.AsyncHTTPClient(io_loop=tornado.ioloop.IOLoop.instance())
            #print "yielding"
            response = yield tornado.gen.Task(http_client.fetch, outbound_request)
            print response

            message = "You requested %s\n" % "hi"
            request.write("HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n%s" % (len(message), message))
            request.finish()


            #if response.code == 200:
            #    print "got a 200"
            #else:
            #    print "got something other than a 200"
        except Exception as e:
            print "Unexpected error:", e

app = tornado.web.Application([
    (r"/", AwesomeHandler)
])
http_server = tornado.httpserver.HTTPServer(app)
http_server.listen(8888)
#tornado.ioloop.IOLoop.instance().start()
