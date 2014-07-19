from __future__ import absolute_import
from tornado import gen
from datetime import datetime
from restless.preparers import FieldsPreparer
from .base import BaseResource, UserMixin
from ...tasks import user, utils
from ...models import User
from miitus import defs


class UserResource(BaseResource, UserMixin):
    """
    User resource
    """
    __mts_route__ = [('/r/users', 'list')]

    preparer = FieldsPreparer(fields={
        'id': 'id.int',
        'email': 'email',
        'gender': 'gender',
        'b_day': 'b_day',
        'nation': 'nation'
    })

    @gen.coroutine
    def create(self):
        """
        """
        u = User(
            email=self.r_handler.json_args.get('email'),
            password=self.core.hasher(self.r_handler.json_args.get('password')),
            gender=self.r_handler.json_args.get('gender'),
            nation=self.r_handler.json_args.get('loc'),
            b_day=datetime.strptime(self.r_handler.json_args.get('b_day'), '%Y-%m-%d'),
            joinTime=datetime.now()
        )

        # would raise ValidationError is not valid
        u.validate()

        u.id = yield gen.Task(self.r_handler.wait_for_result, utils.gen_dist_uuid.si(defs.SEQ_USER).delay())
        yield gen.Task(self.r_handler.wait_for_result,
            user.create_new_user.si(u.id, u.email, u.password, u.gender, u.nation, u.b_day, u.joinTime).delay())
        passed = yield gen.Task(self.r_handler.wait_for_result, user.check_user_password.si(u.email, u.password).delay())
        if passed:
            u = u.to_dict()

            self.login_user(u)
            raise gen.Return(u)

    def detail_list(self):
        """
        get an arbitary user's resource object
        """
        self.send_error(404)

