from __future__ import absolute_import
from tornado.web import RestHandler
from tornado import gen
from ...tasks import user
from ...models import User
from ...utils import UserMixin
from miitus.srv import exceptions
from miitus.srv.rest import err


class Session(RestHandler, UserMixin):
    """
    Login User
    """
    __route__ = ['/r/sessions'] 
    def get(self):
        """
        a login attempt via token stored in session-cookie
        """
        try:
            u = self.get_secure_cookie('user')
            if u:
                self.push_obj('user', u)
                self.set_status(200)
            else:
                self.set_status(401, reason="Unauthorized")

        except Exception as e:
            self.add_err(e)
            self.push_obj('status', {'code': err.failed})
            self.set_status(500)
        finally:
            self.flush()


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

        except exceptions.PasswordWrong:
            self.set_status(401, reason="Invalid Password Or Email")

        except Exception as e:
            self.add_err(e)
            self.push_obj('status', {'code': err.failed})
            self.set_status(500)
        finally:
            self.flush()

    def delete(self):
        """
        a logout attempt
        """
        self.logout_user()

        self.set_status(200)
        self.push_obj('status', {'code': err.success})
        self.flush()

