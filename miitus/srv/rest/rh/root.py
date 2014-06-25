from __future__ import absolute_import
from tornado.web import RequestHandler
import miitus.defs


class Root(RequestHandler):
    """
    when accessing root: '/'
    """
    
    __route__ = ['/']

    def get(self):
        self.redirect(miitus.defs.STATIC_URL_PREFIX + miitus.defs.INDEX_PAGE)

