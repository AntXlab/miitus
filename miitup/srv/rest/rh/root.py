from __future__ import absolute_import
from tornado.web import RequestHandler
import miitup.defs

class RootHandler(RequestHandler):
    """
    when accessing root: '/'
    """
    def get(self):
        self.redirect(miitup.defs.STATIC_URL_PREFIX + miitup.defs.INDEX_PAGE)

