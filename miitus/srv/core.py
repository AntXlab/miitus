from celery import Celery
from cqlengine import connection
from itsdangerous import URLSafeTimedSerializer
from werkzeug.utils import find_modules
from six import string_types
from .util import Singleton, Config, Hasher
from miitus import defs


class Core(Singleton):
    """
    containing everything needs one-time initialization
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

    def __init__(self):
        """
        """
        c = Config()

        self.__app = Celery(
            c['CELERY_MAIN_NAME'],
            broker=c['CELERY_BROKER_URL'],
            backend=c['CELERY_BACKEND_URL'],
            include=c['CELERY_MODULES_INCLUDE'].extend(Core.__gen_task_include(defs.TASK_PACKAGE_ROOT))
        )

        connection.setup(hosts=c['CQLENGINE_HOSTS'])

        self.__serializer = URLSafeTimedSerializer(c['TOKEN_SECRET_KEY'])

        self.__hasher = Hasher(c['HASH_SECRET_KEY'])

    @property
    def worker(self):
        """
        get celery app
        """
        return self.__app

    @property
    def serializer(self):
        """
        get serializer
        """
        return self.__serializer
    
    @property
    def hasher(self):
        """
        get hasher
        """
        return self.__hasher


# for celeryd
__celery_app = Core().worker

