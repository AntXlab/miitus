import tornado.ioloop
from miitup.srv.rest.app import app as app

if __name__ == '__main__':
    app.listen(9001)
    tornado.ioloop.IOLoop.instance().start()

