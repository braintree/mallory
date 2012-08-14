import mallory
import tornado.httpserver
import tornado.web

class Server:
    def __init__(self, proxy_to, port, http_request_options, ssl_options):
        circuit_breaker = mallory.CircuitBreaker(proxy_to)
        app = tornado.web.Application([
            (r"/_mallory/heartbeat", mallory.HeartbeatHandler, dict(circuit_breaker=circuit_breaker)),
            (r"/.*", mallory.RequestHandler, dict(circuit_breaker=circuit_breaker, proxy_to=proxy_to, http_request_options=http_request_options))
        ])
        self.http_server = tornado.httpserver.HTTPServer(app, ssl_options=ssl_options)
        self.port = port

    def start(self):
        self.http_server.listen(self.port, address="0.0.0.0")

    def stop(self):
        self.http_server.stop()
