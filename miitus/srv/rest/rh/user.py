from __future__ import absolute_import
from tornado.web import RequestHandler
from tornado import gen
from .base import RestHandler
from ...tasks import user
from ...models import User

from datetime import datetime

class UserResource(RestHandler):
    """
    User resource
    """
    __route__ = ['/r/users']

    @gen.coroutine
    def post(self):
        u = User(
            email=self.json_args.get('email'),
            password=self.core.hasher(self.json_args.get('password')),
            gender=self.json_args.get('gender'),
            nation=self.json_args.get('loc'),
            bDay=datetime.strptime(self.json_args.get('bday'), '%Y-%m-%d'),
            joinTime=datetime.now()
        )
        u.validate()
        t = user.create_new_user.delay(u.email, u.password, u.gender, u.nation, u.bDay, u.joinTime)
        result = yield gen.Task(self.wait_for_result, t)
        # TODO: result handling

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

