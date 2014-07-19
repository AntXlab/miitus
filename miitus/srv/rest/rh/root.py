from __future__ import absolute_import
from tornado.web import RequestHandler
from miitus import defs


class Root(RequestHandler):
    """
    when accessing root: '/'
    """
    
    __mts_route__ = ['/']

    def get(self):
        self.redirect(defs.STATIC_WEB_URL_PREFIX + defs.INDEX_PAGE)

