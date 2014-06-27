from __future__ import absolute_import
from tornado.web import RequestHandler, HTTPError
from ..core import Core
from ..util import CeleryResultMixin
import json


class BaseHandler(RequestHandler, CeleryResultMixin):
    """
    base of all request-handler
    """
    def initialize(self):
        super(BaseHandler, self).initialize()
        self.__core = Core()


class RestHandler(BaseHandler):
    """
    request handler that handle IO in rest-style
    """
    def prepare(self):
        super(RestHandler, self).prepare()

        content_type = self.request.headers.get('Content-Type')
        if content_type.startswith('application/json'):
            # handle media-type: json
            if content_type.rfind('charset=UTF-8'):
                self.json_args = json.loads(self.request.body, encoding='utf-8')
            else:
                raise HTTPError('unsupported application type:' + content_type)

