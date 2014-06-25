from __future__ import absolute_import
from tornado.web import RequestHandler, HTTPError
from ..core import Core
import json


class Base(RequestHandler):
    """
    base of all request-handler
    """
    def initialize(self):
       super(Base, self).initialize()

       self.core = Core()

class Json(Base):
    """
    request handler that handle json content
    """
    def prepare(self):
        super(Json, self).prepare()

        content_type = self.request.headers.get('Content-Type')
        if content_type.startswith('application/json'):
            # handle media-type: json

            if content_type.rfind('charset=UTF-8'):
                self.json_args = json.loads(self.request.body, encoding='utf-8')
            else:
                raise HTTPError('unsupported application type:' + content_type)

