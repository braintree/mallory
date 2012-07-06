import socket
import tornado.ioloop
import tornado.iostream
import urlparse

class CircuitBreaker:
    def __init__(self, proxy_to_string):
        proxy_to = urlparse.urlparse(proxy_to_string)

        self.history = []
        self.reset_timer = tornado.ioloop.PeriodicCallback(self._attempt_to_reset, 1000)
        self.host = proxy_to.hostname
        self.port = self._determine_port(proxy_to)

    def is_tripped(self):
        return self.history == [False, False, False]

    def report_error(self):
        self._record_result(False)
        if self.is_tripped():
            self.reset_timer.start()

    def report_success(self):
        self._record_result(True)
        if not self.is_tripped():
            self.reset_timer.stop()

    def _attempt_to_reset(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        stream = tornado.iostream.IOStream(s)
        stream.connect((self.host, self.port), self.report_success)

    def _determine_port(self, proxy_to):
        if proxy_to.port:
            return proxy_to.port

        if proxy_to.scheme == "https":
            return 443
        else:
            return 80

    def _record_result(self, check_successful):
        self.history.append(check_successful)
        if len(self.history) > 3:
            self.history.pop(0)
