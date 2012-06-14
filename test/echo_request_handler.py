import tornado
import tornado.web
import tornado.gen
import re

class EchoRequestHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def handle_request(self):
        try:
            message = "PATH: %s\n" % self.request.path
            message += "QUERY STRING: %s\n" % self.request.query
            message += "METHOD: %s\n" % self.request.method
            message += "BODY: %s\n" % self.request.body

            for key, value in self.request.headers.iteritems():
                message += "%s: %s\n" % (key, value)

            if self.request.path.find("/http_status") == 0:
                status = int(re.search("/http_status/(\d+)", self.request.path).group(1))
            else:
                status = 200

            self.set_status(status)
            self.set_header('Content-Length', len(message))
            self.set_header('X-Requested-Method', self.request.method)

            if self.request.path.find("/http_header") == 0:
                match = re.search("/http_header/(.+)/(.+)", self.request.path)
                self.set_header(match.group(1), match.group(2))

            self.write(message)
            self.finish()

        except Exception as e:
            print "Unexpected error:", e

    get = post = head = delete = put = handle_request
