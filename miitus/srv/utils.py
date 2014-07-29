from __future__ import absolute_import
from werkzeug.utils import import_string, find_modules
from os import path
from datetime import timedelta
from tornado.ioloop import IOLoop
from tornado import stack_context
from six import string_types
from miitus import const
import hashlib
import functools
import json
import uuid
import contextlib


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

    objects inside should be thread-safe, because this class didn't provide that
    promise.
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

    def override_config(self, package_name):
        """
        """
        for name in find_modules(package_name, recursive=True):
            self.from_object(name)

    def __init__(self, package_name=None):
        """ import default config, and apply required patches """
        package_name = package_name or const.PACKAGE_ROOT

        self.from_object(package_name + '.config.base')
        self.from_object(package_name + '.config.patch')
        self.override_config(package_name + '.config.override')

        # import task-modules
        self['CELERY_CONF_CELERY_IMPORTS'].extend(Config.__gen_task_include(const.TASK_PACKAGE_ROOT))

    def from_object(self, obj):
        """
        refer to flask.config.from_object
        """
        obj = import_string(obj, silent=True)
        for k in dir(obj):
            if not k.startswith('_'):
                self[k] = getattr(obj, k)

    def to_dict(self, prefix_filter=None, remove_prefix=True):
        """
        """
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

    def __getattr__(self, attr):
        """ access dict as object, readonly """
        return self[attr]



def get_static_web_folder():
    """
    """
    return path.join(path.join(path.join(path.dirname(path.dirname(path.dirname(__file__))), 'client'), 'web'), 'app')

def get_static_api_doc_folder():
    """
    """
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


class CQLHelperMixin(object):
    """
    """
    def to_dict(self):
        """
        I'm not sure if the '_' means they want it private.
        Thus I create a helper class to wrap it. Once it's private
        in the future, I would roll one on my own.
        """
        return self._as_dict()


class SQLHelperMixin(object):
    """
    """
    def to_dict(self):
        """
        """
        ret = {}

        for k in self.__table__.columns.keys():
            ret[k] = getattr(self, k, None)
            # TODO: handle relationship

        return ret


class __UUIDEncoder(json.JSONEncoder):
    """ json encoder for UUID """
    def default(self, o):
        if isinstance(o, uuid.UUID):
            return o.hex
        return json.JSONDecoder.default(self, o)


def json_encode(value):
    """ json encode a python object """
    # please refer to tornado.escape.json_encode,
    # what we add here is a customization to UUID support
    return json.dumps(value, cls=__UUIDEncoder).replace("</", "<\\/")


@contextlib.contextmanager
def session_scope(session_factory, expire=True):
    """
    From SQLAlchemy tutorial,
    Provide a transactional scope around a series of operations.

        http://docs.sqlalchemy.org/en/latest/orm/session.html#unitofwork-contextual
    """
    session = session_factory()
    session.expire_on_commit = expire
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

