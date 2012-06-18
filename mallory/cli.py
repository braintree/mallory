import logging
import mallory
import mallory.logs
import optparse
import os
import signal
import sys
import tornado.ioloop

def start(args):
    parser = optparse.OptionParser(usage="mallory [options] target")
    parser.add_option("-p", "--port", dest="port", default=9000)
    parser.add_option("--verify-ca-cert", dest="ca_cert", help="CA certificate to verify on backend")
    parser.add_option("--ssl-key", dest="ssl_key", help="Private key for serving SSL")
    parser.add_option("--ssl-cert", dest="ssl_cert", help="Certificate for serving SSL")
    parser.add_option("--proxy-request-timeout", dest="proxy_request_timeout", default=20, type="float", help="Proxy timeout in seconds")

    (options, params) = parser.parse_args(args)

    mallory.logs.setup()
    server = mallory.Server(proxy_to=params[0], port=options.port, ca_file=options.ca_cert, request_timeout=options.proxy_request_timeout, ssl_options={ "certfile": options.ssl_cert, "keyfile": options.ssl_key })
    handle_interrupt(server)

    logging.info("starting mallory on port %s" % options.port)
    server.start()

    tornado.ioloop.IOLoop.instance().start()

def handle_interrupt(server):
    def signal_handler(signal, frame):
        server.stop()
        logging.info('stopping mallory...')
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

