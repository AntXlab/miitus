from celery import Celery
from celery.signals import worker_process_init
from cqlengine import connection
from itsdangerous import URLSafeTimedSerializer
from .utils import Singleton, Config, Hasher
from miitus import defs


@worker_process_init.connect
def _init_db_connection(**kwargs):
    """
    Please refer to the link below to find out why we didn't establish
    db connection in __init__
        
        http://www.dctrwatson.com/2010/09/python-thread-safe-does-not-mean-fork-safe/

    In short, the db-connection handle of parent process would be copied to memory
    of child process by fork.
    """
    c = Config()
    
    # this callback can't execute longer than 4 seconds, or would be interrupted by
    # celery
    connection.setup(hosts=c['CQLENGINE_HOSTS'], default_keyspace=defs.CQL_KEYSPACE_NAME)


class Core(Singleton):
    """
    containing everything needs one-time initialization
    """

    def __init__(self):
        """
        """
        c = Config()

        self.__app = Celery(
            c['CELERY_MAIN_NAME'],
            broker=c['CELERY_BROKER_URL'],
            backend=c['CELERY_BACKEND_URL']
        )

        self.__app.config_from_object(c.to_dict(prefix_filter=defs.CELERY_CONFIG_PREFIX))
        self.__serializer = Serializer(c['TOKEN_SECRET_KEY'], c['MAX_AGE'])
        self.__hasher = Hasher(c['HASH_SECRET_KEY'])

        if defs.CELERY_ALWAYS_EAGER in c and c[defs.CELERY_ALWAYS_EAGER] == True:
            # TODO: better way to handle this case is lazy-loading, however, it's 
            # a feature not merged to master branch of cqlegine, would be merged
            # in 0.16.
            _init_db_connection()

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


class Serializer(object):

    def __init__(self, secret, max_age):
        self.__max_age = max_age
        self.__serializer = URLSafeTimedSerializer(secret)

    def loads(self, token):
        return self.__serializer(token, max_age=self.__max_age)

    def dumps(self, data):
        return self.__serializer(data)

# for celery worker
__celery_app = Core().worker

