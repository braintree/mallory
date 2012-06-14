import optparse
import mallory
import mallory.logs
import tornado.ioloop
import signal
import sys

def start(args):
    parser = optparse.OptionParser(usage="mallory [options] target")
    parser.add_option("-p", "--port", dest="port", default=9000)
    parser.add_option("--verify-ca-cert", dest="ca_cert", help="CA certificate to verify on backend")
    parser.add_option("--ssl-key", dest="ssl_key", help="Private key for serving SSL")
    parser.add_option("--ssl-cert", dest="ssl_cert", help="Certificate for serving SSL")

    (options, params) = parser.parse_args(args)


    mallory.logs.setup()
    server = mallory.Server(proxy_to=params[0], port=options.port, ca_file=options.ca_cert, ssl_options={ "certfile": options.ssl_cert, "keyfile": options.ssl_key })
    handle_interrupt(server)

    server.start()
    tornado.ioloop.IOLoop.instance().start()

def handle_interrupt(server):
    def signal_handler(signal, frame):
        server.stop()
        print 'You pressed Ctrl+C!'
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

