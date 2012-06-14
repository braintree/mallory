import mallory
import tornado.httpserver
import tornado.web

class Server:
    def __init__(self, proxy_to, ca_file, port, **httpserver_kwargs):
        app = tornado.web.Application([
            (r"/.*", mallory.RequestHandler, dict(proxy_to=proxy_to, ca_file=ca_file))
        ])
        self.http_server = tornado.httpserver.HTTPServer(app, **httpserver_kwargs)
        self.port = port

    def start(self):
        self.http_server.listen(self.port, address="0.0.0.0")

    def stop(self):
        self.http_server.stop()

