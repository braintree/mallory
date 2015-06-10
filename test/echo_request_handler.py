import cStringIO
import gzip
import re
import time
import tornado
import tornado.gen
import tornado.web

class EchoRequestHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def handle_request(self):
        try:
            if self.request.path.find("/timeout") == 0:
                return

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
            self.set_header('X-Requested-Method', self.request.method)

            if self.request.path.find("/http_header") == 0:
                match = re.search("/http_header/(.+)/(.+)", self.request.path)
                self.set_header(match.group(1), match.group(2))

            if self.request.path.find("/gzip") == 0:
                compressed_message = self._gzip(message)
                self.set_header('Content-Length', len(compressed_message))
                self.set_header('Content-Encoding', 'gzip')
                self.write(compressed_message)
            else:
                self.set_header('Content-Length', len(message))
                self.write(message)

            self.finish()

        except Exception as e:
            print "Unexpected test harness error:", e

    get = post = head = delete = put = patch = handle_request

    def _request_summary(self):
        return "(Echo Handler) %s %s (%s)" % (self.request.method,  self.request.path, self.request.remote_ip)

    def _gzip(self, data):
        gzip_buffer = cStringIO.StringIO()
        gzip_file = gzip.GzipFile(mode='wb', fileobj=gzip_buffer)
        gzip_file.write(data)
        gzip_file.close()
        return gzip_buffer.getvalue()
