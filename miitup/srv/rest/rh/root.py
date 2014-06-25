from __future__ import absolute_import
from tornado.web import RequestHandler
import miitup.defs


class Root(RequestHandler):
    """
    when accessing root: '/'
    """
    
    __route__ = ['/']

    def get(self):
        self.redirect(miitup.defs.STATIC_URL_PREFIX + miitup.defs.INDEX_PAGE)

