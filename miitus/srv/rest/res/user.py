from __future__ import absolute_import
from tornado import gen
from restless.preparers import FieldsPreparer
from ..base import BaseResource, UserMixin
from ...tasks import user
from ...models.sql import User


class UserResource(BaseResource, UserMixin):
    """
    User resource
    """
    __mts_route__ = [('/r/users', 'list')]

    preparer = FieldsPreparer(fields={
        'id': 'id',
        'email': 'email',
    })

    @gen.coroutine
    def create(self):
        """
        """
        # trigger validation before sending to backend.
        u = User(
            email=self.r_handler.json_args.get('email'),
            password=self.runtime.hasher(self.r_handler.json_args.get('password')),
        )

        obj = u.to_dict()
        ret = yield gen.Task(self.r_handler.wait_for_result,
            user.create_new_user.si(obj).delay())

        self.login_user(ret)
        raise gen.Return(ret)

    def detail_list(self):
        """
        get an arbitary user's resource object
        """
        self.send_error(404)

