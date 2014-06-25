from __future__ import absolute_import
from tornado.web import RequestHandler
from .base import Base, Json


class UserResource(Json):
    """
    User resource
    """
    __route__ = ['/r/users']

    def post(self):
        email = self.json_args.get('email')
        # hash password before passing to anywhere
        password = self.core.hasher(self.json_args.get('login_psswd'))
        gender = self.json_args.get('gender')
        loc = self.json_args.get('loc')
        bday = self.json_args.get('bday')

        self.send_error(404)

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

