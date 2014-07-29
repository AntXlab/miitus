from __future__ import absolute_import
from tornado import testing
from miitus.srv.rest.app import App


class BaseTestCase(testing.AsyncHTTPTestCase):
    """
    """
    def get_app(self):
        """ return tornado app module """
        return App().app

