import mallory
import tornado.httpserver
import tornado.web

class Server:
    def __init__(self, proxy_to, ca_file, port, request_timeout, **httpserver_kwargs):
        circuit_breaker = mallory.CircuitBreaker(proxy_to)
        app = tornado.web.Application([
            (r"/_mallory/heartbeat", mallory.HeartbeatHandler, dict(circuit_breaker=circuit_breaker)),
            (r"/.*", mallory.RequestHandler, dict(circuit_breaker=circuit_breaker, proxy_to=proxy_to, ca_file=ca_file, request_timeout=request_timeout))
        ])
        self.http_server = tornado.httpserver.HTTPServer(app, **httpserver_kwargs)
        self.port = port

    def start(self):
        self.http_server.listen(self.port, address="0.0.0.0")

    def stop(self):
        self.http_server.stop()

