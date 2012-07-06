import tornado.web
import mallory

class HeartbeatHandler(tornado.web.RequestHandler):
    def initialize(self, circuit_breaker):
        self.circuit_breaker = circuit_breaker

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        if self.circuit_breaker.is_tripped():
            self.set_status(503)
        else:
            self.set_status(200)

        self.write("Mallory " + mallory.Version + "\n")
        self.write("OK")
        self.finish()
