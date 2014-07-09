from __future__ import absolute_import
from werkzeug.utils import import_string
from os import path
from datetime import timedelta
from tornado.ioloop import IOLoop
from tornado import stack_context
from tornado.escape import json_encode
from werkzeug.utils import find_modules
from six import string_types
from miitus import defs
import hashlib
import functools


class _Singleton(type):
    _instance = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instance[cls]


class Singleton(_Singleton('SingletonMeta', (object,), {})):
    """
    a singleton implementation, refer to
        http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    """
    pass


class Config(Singleton, dict):
    """
    config object
    """

    @staticmethod
    def __gen_task_include(package_name):
        """ scan miitus/srv/tasks folder to include those modules """
        if not isinstance(package_name, string_types):
            raise TypeError(
                'Only accept string-types for package_name, not:' + str(package_name)
            )

        ret = []
        for name in find_modules(package_name, recursive=True):
            ret.append(name)

        return ret


    def __init__(self, package_name=None):
        """ import default config, and apply required patches """
        package_name = package_name or defs.PACKAGE_ROOT
        config_name = package_name + '.config'

        self.from_object(config_name)

        # import task-modules
        self['CELERY_CONF_CELERY_IMPORTS'].extend(Config.__gen_task_include(defs.TASK_PACKAGE_ROOT))

    def from_object(self, obj):
        """
        refer to flask.config.from_object
        """
        obj = import_string(obj, silent=True)
        for k in dir(obj):
            if not k.startswith('_'):
                self[k] = getattr(obj, k)

    def to_dict(self, prefix_filter=None, remove_prefix=True):
        if not isinstance(prefix_filter, string_types):
            raise TypeError('only accept str for prefix_filter')
        ret = {}
        for k in self:
            if k.startswith(prefix_filter):
                if remove_prefix:
                    ret[k[len(prefix_filter):]] = self[k]
                else:
                    ret[k] = self[k]
        return ret


def get_static_web_folder():
    return path.join(path.join(path.join(path.dirname(path.dirname(path.dirname(__file__))), 'client'), 'web'), 'app')

def get_static_api_doc_folder():
    return path.join(path.join(path.dirname(path.dirname(path.dirname(__file__))), 'docs'), 'swagger')


class Hasher(object):
    """
    man doing hash
    """
    def __init__(self, key):
        self.__key = key

    def __call__(self, data):
        m = hashlib.sha1()
        m.update(data)
        m.update(self.__key)
        return m.hexdigest()


class CeleryResultMixin(object):
    """
    Helper for checking celery result asynchrounsly.

    please refer to
        http://stackoverflow.com/questions/8202282/tornado-celery-integration-hacks

    for more details about 'why' of this class.
    """

    def wait_for_result(self, task, callback):
        if task.ready():
            callback(task.result)
        else:
            # TODO: different time-out value for each kind of task
            IOLoop.instance().add_timeout(
                timedelta(seconds=1),
                functools.partial(
                    stack_context.wrap(self.wait_for_result), task, callback
                )
            )


def return_exception(t):                                                           
    """
    When using celery-chain, once exception, the later
    task won't be called, and normal usage of result.get()
    would just hang there.
    """
    @functools.wraps(t)                                                                  
    def inner(*args, **kwargs):                                                
        exps = [arg for arg in args if issubclass(type(arg), Exception)]
        if len(exps) > 0:
            return exps[0]

        try:
            return t(*args, **kwargs)
        except Exception as e:
            return e

    return inner


class UserMixin(object):
    """
    """
    def login_user(self, user_obj):
        """
        login user,
        note we usually use shorter expired day than normal token
        """
        if not hasattr(self, '__user_cookie_duration'):
            self.__user_cookie_duration = Config()['USER_COOKIE_DURATION']

        if not isinstance(user_obj, dict):
            raise TypeError('user_obj should be dict')

        if not ('email' in user_obj and 'password' in user_obj):
            raise ValueError('password or email is missing in user-obj:' + str(user_obj))

        # set token
        self.core.serializer.dumps([user_obj['email'], user_obj['password']])

        # make sure we won't send raw password through the wire.
        user_obj.pop('password', None)
        self.set_secure_cookie('user', json_encode(user_obj), expires_days=self.__user_cookie_duration)

    def logout_user(self):
        """ logout user """
        self.clear_cookie('user')
        self.clear_cookie('token')


class ModelHelperMixin(object):
    """
    """
    def to_dict(self):
        """
        I'm not sure if the '_' means they want it private.
        Thus I create a helper class to wrap it. Once it's private
        in the future, I would roll one on my own.
        """
        return self._as_dict()

