from __future__ import absolute_import
from tornado.web import RequestHandler, HTTPError
from tornado.escape import json_decode
from ..core import Core
from ..util import CeleryResultMixin
import six
import miitus.defs


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

    def initialize(self):
        super(RestHandler, self).initialize()
        self.__init_envelope()

    def prepare(self):
        """
        According to FAQ of tornado, they won't handle json media-type.
        """
        super(RestHandler, self).prepare()

        content_type = self.request.headers.get('Content-Type')
        if content_type.startswith('application/json'):
            # handle media-type: json
            if content_type.rfind('charset=UTF-8'):
                self.json_args = json_decode(self.request.body)
            else:
                raise HTTPError('unsupported application type:' + content_type)

    def __init_envelope(self):
        self.__rest_envelope = {}
        self.push_obj({
            'version': miitus.defs.REST_VERSION
            })

    def push_obj(self, key, obj):
        if key and isinstance(key, six.string_types):
            self.__rest_envelope[key] = obj

    def flush_objs(self, key=None, obj=None, callback=None):
        if key and isinstance(key, six.string_types):
            self.__rest_envelope[key] = obj

        self.write(self.__rest_envelope)
        self.__init_envelope()
        self.flush(callback=callback)

