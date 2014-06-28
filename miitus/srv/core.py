from celery import Celery
from cqlengine import connection
from itsdangerous import URLSafeTimedSerializer
from .util import Singleton, Config, Hasher


class Core(Singleton):
    """
    containing everything needs one-time initialization
    """
    def __init__(self):
        """
        """
        c = Config()

        self.__app = Celery(
            c['CELERY_MAIN_MODULE'],
            broker=c['CELERY_BROKER_URL'],
            backend=c['CELERY_BACKEND_URL']
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

