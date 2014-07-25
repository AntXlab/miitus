from __future__ import absolute_import
from os import path
from tornado.web import RequestHandler, HTTPError, StaticFileHandler
from tornado.escape import json_decode
from ..core import Runtime
from ..utils import CeleryResultMixin, Config, json_encode
from restless.tnd import TornadoResource
from miitus.srv import exc
import sqlalchemy.exc


class BaseHandler(RequestHandler, CeleryResultMixin):
    """
    base of all request-handler
    """
    def initialize(self):
        super(BaseHandler, self).initialize()

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


class BaseResource(TornadoResource):
    """
    """
    _request_handler_base_ = RestHandler

    def __init__(self, *args, **kwargs):
        super(BaseResource, self).__init__(*args, **kwargs)
        self.runtime = Runtime()

    def is_authenticated(self):
        """ use tornado's authentication instead """
        return True

    def build_error(self, err):
        """
        method to convert internal error to http error
        """
        err = self.__convert_exception(err) if not self.is_debug() else err
        return super(BaseResource, self).build_error(err)

    @staticmethod
    def __convert_exception(err):
        """
        normalize exceptions
        """
        if isinstance(err, sqlalchemy.exc.IntegrityError):
            return exc.ConflictError()


class SwaggerJsonFileHandler(StaticFileHandler):
    """
    """
    def parse_url_path(self, url_path):
        if len(url_path) == 0:
            return 'resource_list.json'
        return path.join('res', (url_path + '.json'))


class UserMixin(object):
    """
    """
    def login_user(self, user_obj):
        """
        login user,
        note we usually use shorter expired day than normal token
        """
        conf = Config()
        if not hasattr(self, '__user_cookie_duration'):
            self.__user_cookie_duration = conf.USER_COOKIE_DURATION
        if not hasattr(self, '__token_cookie_duration'):
            self.__token_cookie_duration = conf.TOKEN_COOKIE_DURATION


        if not isinstance(user_obj, dict):
            raise TypeError('user_obj should be dict')

        if not ('email' in user_obj and 'password' in user_obj):
            raise ValueError('password or email is missing in user-obj:' + str(user_obj))

        local_obj = user_obj.copy()

        # set token
        self.r_handler.set_secure_cookie('token',
            self.core.serializer.dumps([local_obj['email'], local_obj['password']]),
            expires_days=self.__token_cookie_duration)

        # make sure we won't send raw password through the wire.
        local_obj.pop('password', None)
        self.r_handler.set_secure_cookie('user', json_encode(local_obj), expires_days=self.__user_cookie_duration)

    def logout_user(self):
        """ logout user """
        self.clear_cookie('user')
        self.clear_cookie('token')

