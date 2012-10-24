from tornado import ioloop
from tornado import httpserver
from tornado import gen
import tornado.autoreload
from tornado import web
from tornado.options import define, options
import os
import serial

define("serial", default="/dev/ttyACM0", help="Serial port")


class MainHandler(web.RequestHandler):
    def get(self):
        print "options"
        print options.serial
        self.render("index2.html")


class ServoHandler(web.RequestHandler):
    def get(self):
        servo = self.get_argument("servo", default=None, strip=False)
        s = serial.Serial(options.serial, 9600)
        s.write(servo)
        self.write('ok')


class LedHandler(web.RequestHandler):
    @web.asynchronous
    def get(self):
        led = self.get_argument("led", default=None, strip=False)
        s = serial.Serial(options.serial, 9600)
        result = s.write(led)
        self._read_serial(result, s)

    #TODO : ajouter handler pour eviter le timeout
    def _read_serial(self, reponse, serial):
        status = serial.read()
        self.write(unicode(status))
        self.finish()


class Application(web.Application):
    """application definition and url mapping"""
    def __init__(self):
        settings = dict(
                    static_path=os.path.join(
                        os.path.dirname(__file__), "static"),
                    cookie_secret="32oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
                    #login_url="/auth/",
                    debug="True",
                    )
        handlers = [
                        (r"/", MainHandler),
                        (r"/led", LedHandler),
                        (r"/servo", ServoHandler),
                        #(r"/store", StoreHandler),
                        #(r"/auth/", AuthHandler),
                        #(r"/auth/login", LoginHandler),
                        #(r"/auth/logout", LogoutHandler),
                        #(r"/admin", AdminHandler),
                        (r"(/static/)",  tornado.web.StaticFileHandler,
                        dict(path=settings['static_path']))
                       ]
        web.Application.__init__(self, handlers, **settings)


def main():
    app = Application()
    options.parse_command_line()
    app.listen(8888)
    io_loop = ioloop.IOLoop.instance().start()
    tornado.autoreload.start(io_loop)

if __name__ == "__main__":
    main()
