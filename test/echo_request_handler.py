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

            for key, value in self.request.headers.iteritems():
                message += "%s: %s\n" % (key, value)

            if self.request.path.find("/http_status") == 0:
                status = int(re.search("/http_status/(\d+)", self.request.path).group(1))
            else:
                status = 200

            self.set_status(status)
            self.set_header('Content-Length', len(message))

            if self.request.path.find("/http_header") == 0:
                match = re.search("/http_header/(.+)/(.+)", self.request.path)
                self.set_header(match.group(1), match.group(2))

            self.write(message)
            self.finish()

        except Exception as e:
            print "Unexpected error:", e


