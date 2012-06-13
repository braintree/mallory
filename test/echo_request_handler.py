import tornado
import tornado.web
import tornado.gen

class EchoRequestHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        try:
            # todo: request method, path_info, query_string, post body
            message = "PATH: %s\n" % self.request.path
            #for key in request.headers:
            #    message += ("%s: %s" % [key, request.headers[key]])

            self.write("HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n%s" % (len(message), message))
            self.finish()

        except Exception as e:
            print "Unexpected error:", e


