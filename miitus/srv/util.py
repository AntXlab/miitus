from __future__ import absolute_import
from werkzeug.utils import import_string
from os import path
from datetime import timedelta
from tornado.ioloop import IOLoop
from tornado import stack_context
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
    def __init__(self, package_name=None):
        # import default config
        package_name = package_name or defs.PACKAGE_ROOT
        config_name = package_name + '.config'

        self.from_object(config_name)

    def from_object(self, obj):
        """
        refer to flask.config.from_object
        """
        obj = import_string(obj, silent=True)
        for k in dir(obj):
            if not k.startswith('_'):
                self[k] = getattr(obj, k)

    def to_dict(self, prefix_filter=None):
        if not isinstance(prefix_filter, string_types):
            raise TypeError('only accept str for prefix_filter')
        ret = {}
        for k in self:
            if k.startswith(prefix_filter):
                ret[k[len(prefix_filter):]] = self[k]
        return ret


def get_static_folder():
    return path.join(path.join(path.join(path.dirname(path.dirname(path.dirname(__file__))), 'client'), 'web'), 'app')


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

