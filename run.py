import tornado.ioloop
from miitus.srv.rest.app import App
from miitus.srv.tasks import management
from miitus.srv.core import Core


if __name__ == '__main__':
    # init db, becaue in eagar mode, we need
    c = Core()
    # do management task before running
    t = management.prepare_db.delay()
    t.wait()

    App().app.listen(9001)
    tornado.ioloop.IOLoop.instance().start()

