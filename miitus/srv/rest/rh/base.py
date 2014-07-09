from __future__ import absolute_import
from os import path
from tornado.web import RequestHandler, HTTPError, StaticFileHandler
from tornado.escape import json_decode
from ...core import Core
from ...utils import CeleryResultMixin
from miitus import defs

import traceback
import six



class BaseHandler(RequestHandler, CeleryResultMixin):
    """
    base of all request-handler
    """
    def initialize(self):
        super(BaseHandler, self).initialize()
        self.core = Core()

    def get_current_user(self):
        """ get current user from session """
        u = self.get_secure_cookie('user')
        u = u and json_decode(u)
        if not isinstance(u, dict):
            raise TypeError('cracked cookie, unknown type of user-object: ' + str(u))

        return u


class RestHandler(BaseHandler):
    """
    request handler that handle IO in rest-style
    """

    """
    Overrided Part
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
        if content_type and content_type.startswith('application/json'):
            # handle media-type: json
            if content_type.rfind('charset=UTF-8'):
                self.json_args = json_decode(self.request.body)
            else:
                raise HTTPError('unsupported application type:' + content_type)

    def write_error(self, status_code, **kwargs):
        # almost identical to original procedure in tornaod, except
        # that we need to write error into envelope first.
        if self.settings.get('serve_traceback') and 'exc_info' in kwargs:
            self.add_err({'msg': traceback.format_exception(*kwargs['exc_info'])})
        else:
            self.add_err({'code': status_code, 'msg': self._reason})

        self.finish()

    def flush(self, include_footers=False, callback=None):
        self.flush_objs()
        return super(RestHandler, self).flush(include_footers, callback)


    """
    New internal func
    """
    def __init_envelope(self):
        self.__rest_envelope = {}
        self.push_obj('meta', {
            'version': defs.REST_VERSION
            })

    """
    New API
    """
    def add_err(self, err):
        errs = self.pop_obj(defs.REST_ERR_OBJ_NAME) or []
        errs.append(err)
        self.push_obj(defs.REST_ERR_OBJ_NAME, errs)

    def pop_obj(self, key):
        return self.__rest_envelope.pop(key, None)

    def push_obj(self, key, obj):
        if key and isinstance(key, six.string_types):
            if key in self.__rest_envelope:
                original = self.__rest_envelope[key]
                if isinstance(original, dict) and isinstance(obj, dict):
                   original.update(obj)
                elif isinstance(original, list) and isinstance(obj, list):
                   original.append(obj)
                else:
                    self.__rest_envelope[key] = obj
            else:
                self.__rest_envelope[key] = obj
        else:
            raise TypeError('Invalid key type: ' + type(key))

    def flush_objs(self, key=None, obj=None):
        if key and isinstance(key, six.string_types):
            self.__rest_envelope[key] = obj

        if len(self.__rest_envelope) > 1:
            self.write(self.__rest_envelope)
            self.__init_envelope()


class SwaggerJsonFileHandler(StaticFileHandler):
    """
    """
    def parse_url_path(self, url_path):
        if len(url_path) == 0:
            return 'resource_list.json'
        return path.join('res', (url_path + '.json'))

