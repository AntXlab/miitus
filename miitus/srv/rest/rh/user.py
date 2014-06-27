from __future__ import absolute_import
from tornado.web import RequestHandler
from tornado import gen
from cqlengine import exceptions
from .base import Json
from ...tasks import user
from ...models import User

import datetime


class UserResource(Json):
    """
    User resource
    """
    __route__ = ['/r/users']

    gen.coroutine()
    def post(self):
        u = User(
            email=self.json_args.get('email'),
            password=self.core.hasher(self.json_args.get('login_psswd')),
            gender=self.json_args.get('gender'),
            nation=self.json_args.get('loc'),
            bDay=self.json_args.get('bday'),
            joinTime=datetime.datetime.now()
        )

        # validate
        try:
            u.validate()
        except exceptions.ValidationError as e:
            
           


    def get(self):
        self.send_error(404)


class UserLogin(RequestHandler):
    """
    Login User
    """
    __route__ = ['/p/users/login']

    def get(self):
        """
        a login attempt via token stored in session-cookie
        """
        self.send_error(404)

    def post(self):
        """
        a login attempt, email & password should be
        passed via post-data.
        """
        self.send_error(404)


class UserLogout(RequestHandler):
    """
    Logout User
    """
    __route__ = ['/p/users/logout']

    def get(self):
        """
        a logout attempt
        """
        self.send_error(404)

