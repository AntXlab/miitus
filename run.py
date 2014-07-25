import tornado.ioloop
import miitus.libs # init libs
from miitus.srv.rest.app import App
from miitus.srv.tasks import management
from miitus.srv.core import Runtime


if __name__ == '__main__':
    rt = Runtime()
    # init db, becaue in eagar mode, we need
    # do management task before running
    t = management.prepare_db.delay()
    t.wait()

    App().app.listen(9001)
    tornado.ioloop.IOLoop.instance().start()

