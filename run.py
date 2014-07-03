import tornado.ioloop
from miitus.srv.rest.app import App
from miitus.srv.tasks import management


if __name__ == '__main__':
    # do management task before running
    t = management.prepare_db.delay()
    t.wait()

    App().app.listen(9001)
    tornado.ioloop.IOLoop.instance().start()

