import tornado
import tornado.web
import tornado.gen
import re

class EchoRequestHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        try:
            message = "PATH: %s\n" % self.request.path
            message += "QUERY STRING: %s\n" % self.request.query

            if self.request.path.find("/http_status") == 0:
                status = int(re.search("/http_status/(\d+)", self.request.path).group(1))
            else:
                status = 200

            self.set_status(status)
            self.set_header('Content-Length', len(message))
            self.write(message)
            self.finish()

        except Exception as e:
            print "Unexpected error:", e


