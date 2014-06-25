from __future__ import absolute_import
from tornado.web import RequestHandler, HTTPError
import json

class Base(RequestHandler):
    
    def prepare(self):
        content_type = self.request.headers.get('Content-Type')
        if content_type.startswith('application/json'):
            super(Base, self).prepare()
            # handle media-type: json

            if content_type.rfind('charset=UTF-8'):
                self.json_args = json.loads(self.request.body, encoding='utf-8')
            else:
                raise HTTPError('unsupported application type:' + content_type)

