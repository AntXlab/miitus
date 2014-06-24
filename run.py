import tornado.ioloop
from miitup.srv.rest.app import App

if __name__ == '__main__':
    App().app.listen(9001)
    tornado.ioloop.IOLoop.instance().start()

