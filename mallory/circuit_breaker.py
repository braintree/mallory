import socket
import tornado.ioloop
import tornado.iostream
import urlparse

class CircuitBreaker:
    def __init__(self, proxy_to_string):
        proxy_to = urlparse.urlparse(proxy_to_string)

        self.tripped = False
        self.reset_timer = tornado.ioloop.PeriodicCallback(self.attempt_to_reset, 1)
        self.host = proxy_to.hostname
        self.port = self._determine_port(proxy_to)

    def is_tripped(self):
        return self.tripped

    def reset(self):
        self.tripped = False
        self.reset_timer.stop()

    def trip(self):
        self.tripped = True
        self.reset_timer.start()

    def report_error(self):
        self.trip()

    def report_success(self):
        self.reset()

    def attempt_to_reset(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        stream = tornado.iostream.IOStream(s)
        stream.connect((self.host, self.port), self.reset)

    def _determine_port(self, proxy_to):
        if proxy_to.port:
            return proxy_to.port

        if proxy_to.scheme == "https":
            return 443
        else:
            return 80
