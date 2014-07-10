from __future__ import absolute_import
from tornado import gen
from datetime import datetime
from .base import RestHandler, UserMixin
from ...tasks import user, utils
from ...models import User
from miitus import defs
from miitus.srv import exceptions
from miitus.srv.rest import err


class UserResource(RestHandler, UserMixin):
    """
    User resource
    """
    __route__ = ['/r/users']

    @gen.coroutine
    def post(self):
        """
        """
        try:
            u = User(
                email=self.json_args.get('email'),
                password=self.core.hasher(self.json_args.get('password')),
                gender=self.json_args.get('gender'),
                nation=self.json_args.get('loc'),
                bDay=datetime.strptime(self.json_args.get('bday'), '%Y-%m-%d'),
                joinTime=datetime.now()
            )

            # would raise ValidationError is not valid
            u.validate()

            u.id = yield gen.Task(self.wait_for_result, utils.gen_dist_uuid.si(defs.SEQ_USER))
            t = (
                user.create_new_user.s(u.id, u.email, u.password, u.gender, u.nation, u.bDay, u.joinTime) |\
                user.check_user_password.si(u.email, u.password)
            ).delay()

            result = yield gen.Task(self.wait_for_result, t)
            if (issubclass(type(result), Exception)):
                raise result

            if result == True:
                self.login_user(u.to_dict())
            else:
                raise exceptions.PasswordWrong('kinda not possible to be here')

            # generate user_obj
            user_obj = u.to_dict()
            user_obj.pop('password', None)
            self.push_obj('user', user_obj)
            self.push_obj('status', {'code': err.success})
            self.set_status(200)

        except exceptions.AlreadyExists as e:
            self.push_obj('status', {'code': err.user_already_exist})
            self.set_status(409, 'User already exists')
        except Exception as e:
            self.add_err(e)
            self.push_obj('status', {'code': err.failed})
            self.set_status(500)
        finally:
            self.flush()


    def get(self):
        """
        get an arbitary user's resource object
        """
        self.send_error(404)

