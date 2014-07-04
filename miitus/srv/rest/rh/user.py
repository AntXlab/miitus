from __future__ import absolute_import
from tornado.web import RequestHandler
from tornado import gen
from datetime import datetime
from .base import RestHandler
from ...tasks import user
from ...models import User
from ...utils import UserMixin
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

            t = (user.create_new_user.si(u.email, u.password, u.gender, u.nation, u.bDay, u.joinTime) |\
                user.check_user_password.si(u.email, u.password)
            ).delay()

            result = yield gen.Task(self.wait_for_result, t)
            if (issubclass(type(result), Exception)):
                raise result

            if result == True:
                self.login_user(u.to_dict())
            else:
                raise exceptions.PasswordWrong('kinda not possible to be here')

            # if nothing goes wrong,
            self.push_obj('user', {'email': u.email})
            self.push_obj('status', {'code': err.success})
            self.set_status(200)

        except exceptions.AlreadyExists as e:
            self.push_obj('status', {'code': err.user_already_exist})
        except Exception as e:
            self.add_err(e)
            self.push_obj('status', {'code': err.failed})
            self.set_status(500)
        finally:
            self.flush()


    def get(self):
        """
        get user resource object
        """
        self.send_error(404)


class UserLogin(RequestHandler, UserMixin):
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
        try:
            u = User(
                email=self.json_args.get('email'),
                password=self.core.hasher(self.json_args.get('password')),
            )

            # would raise ValidationError is not valid
            u.validate()

            t = user.check_user_password(u.email, u.password).delay()
            result = yield gen.Task(self.wait_for_result, t)

            if result == True:
                self.login_user(u.to_dict())
            else:
                raise exceptions.PasswordWrong('kinda not possible to be here')

            # if nothing goes wrong,
            self.push_obj('user', {'email': u.email})
            self.push_obj('status', {'code': err.success})
            self.set_status(200)

        except Exception as e:
            self.add_err(e)
            self.push_obj('status', {'code': err.failed})
            self.set_status(500)
        finally:
            self.flush()


class UserLogout(RequestHandler, UserMixin):
    """
    Logout User
    """
    __route__ = ['/p/users/logout']

    def get(self):
        """
        a logout attempt
        """
        self.logout_user()

        self.set_status(200)
        self.push_obj('status', {'code': err.success})
        self.flush()

