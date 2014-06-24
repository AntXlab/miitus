from celery import Celery
from cqlengine import connection
from .util import Singleton, Config


class Core(Singleton):
    """
    """
    def __init__(self):
        """
        """
        c = Config()

        self.__app = Celery(
            __name__,
            broker=c['CELERY_BROKER_URL'],
            backend=c['CELERY_BACKEND_URL']
        )

        connection.setup(hosts=c['CQLENGINE_HOSTS'])

    @property
    def celery(self):
        """
        get celery app
        """
        return self.__app

