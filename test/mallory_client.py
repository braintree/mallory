import tornado.httpclient

class MalloryClient():
    def __init__(self, port, test_class):
        self.port = port
        self.test_class = test_class
        self.http_client = tornado.httpclient.AsyncHTTPClient()

    def get(self, path, runner):
        url = 'https://127.0.0.1:%s%s' % (self.port, path)
        self.http_client.fetch(url, runner.stop, ca_certs = "test/ssl/server.crt")
        return runner.wait()
