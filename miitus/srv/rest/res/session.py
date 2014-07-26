from __future__ import absolute_import
from tornado import gen
from restless.exceptions import Unauthorized
from restless.preparers import FieldsPreparer
from ..base import BaseResource, UserMixin
from ...tasks import user
from ...models.cql import User


class Session(BaseResource, UserMixin):
    """
    Login User
    """
    __mts_route__ = [('/r/sessions', 'list')]

    preparer = FieldsPreparer(fields={
        'id': 'id',
        'email': 'email',
        'gender': 'gender',
        'b_day': 'b_day',
        'nation': 'nation'
    })

    def list(self):
        """
        a login attempt via token stored in session-cookie
        """
        u = self.r_handler.get_secure_cookie('user')
        if u:
            return u
        else:
            raise Unauthorized()

    @gen.coroutine
    def create(self):
        """
        a login attempt, email & password should be
        passed via post-data.
        """
        u = User(
            email=self.r_handler.json_args.get('email'),
            password=self.runtime.hasher(self.r_handler.json_args.get('password')),
        )

        # would raise ValidationError is not valid
        u.validate()

        t = user.check_user_password.si(u.email, u.password).delay()
        ret = yield gen.Task(self.r_handler.wait_for_result, t)

        if ret:
            self.login_user(ret)
            raise gen.Return(ret)
        else:
            raise Unauthorized()

    def delete_list(self):
        """
        a logout attempt
        """
        self.logout_user()

