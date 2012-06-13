import tornado
import tornado.web
import tornado.gen

class EchoRequestHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(request):
        try:
            # todo: request method, path_info, query_string, post body
            message = "GET: ?\n"
            #for key in request.headers:
            #    message += ("%s: %s" % [key, request.headers[key]])

            request.write("HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n%s" % (len(message), message))
            request.finish()

        except Exception as e:
            print "Unexpected error:", e


