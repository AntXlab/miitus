from __future__ import absolute_import
from tornado.web import RequestHandler
from miitus import const


class Root(RequestHandler):
    """
    when accessing root: '/'
    """
    
    __mts_route__ = ['/']

    def get(self):
        self.redirect(const.STATIC_WEB_URL_PREFIX + const.INDEX_PAGE)

