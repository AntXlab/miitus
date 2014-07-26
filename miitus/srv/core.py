from celery import Celery
from celery.signals import worker_process_init
from cqlengine import connection
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from itsdangerous import URLSafeTimedSerializer
from .utils import Singleton, Config, Hasher
from .prep import Preparation
from miitus import const
import random, time


class Serializer(object):
    """
    Serializer, wrapper for itsdangerous.
    """
    def __init__(self, secret, max_age):
        self.__max_age = max_age
        self.__serializer = URLSafeTimedSerializer(secret)

    def loads(self, token):
        return self.__serializer.loads(token, max_age=self.__max_age)

    def dumps(self, data):
        return self.__serializer.dumps(data)


class Runtime(Singleton):
    """
    containing everything needs one-time initialization
    """

    def __init__(self):
        """
        """
        super(Runtime, self).__init__()

        conf = Config()

        self.__app = Celery(
            conf.CELERY_MAIN_NAME,
            broker=conf.CELERY_BROKER_URL,
            backend=conf.CELERY_BACKEND_URL
        )

        self.__app.config_from_object(conf.to_dict(prefix_filter=const.CELERY_CONFIG_PREFIX))
        self.__serializer = Serializer(conf.TOKEN_SECRET_KEY, conf.MAX_AGE)
        self.__hasher = Hasher(conf.HASH_SECRET_KEY)

        self.__random = random.SystemRandom(time.time())

        # sqlalchemy
        self.__sql_engine = create_engine(conf.SQLALCHEMY_URL, echo=conf.SQLALCHEMY_ECHO)

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

    def random(self, scale=((1 << 32) - 1), base=0):
        """
        get a random number
        """
        return int(self.__random.random() * scale) + base

    @property
    def sql_engine(self):
        """
        get return of create_engine
        """
        return self.__sql_engine

    @property
    def sql_session(self):
        """
        get session maker of sqlalchemy
        """
        return self.__sql_session

    @sql_session.setter
    def sql_session(self, v):
        self.__sql_session = v


# proxy for celery worker
__celery_app = Runtime().worker


@worker_process_init.connect
def _init_db_connection(**kwargs):
    """
    Please refer to the link below to find out why we didn't establish
    db connection in __init__
        
        http://www.dctrwatson.com/2010/09/python-thread-safe-does-not-mean-fork-safe/

    In short, the db-connection handle of parent process would be copied to memory
    of child process by fork.
    """
    conf = Config()

    # this callback can't execute longer than 4 seconds, or would be interrupted by
    # celery
    connection.setup(hosts=conf.CQLENGINE_HOSTS, default_keyspace=const.CQL_KEYSPACE_NAME)

    # sqlalchemy
    rt = Runtime()
    rt.sql_session = sessionmaker(rt.sql_engine)

    # trigger registration of SQLAlchemy models
    from models import sql

    # create tables
    Preparation().Base.metadata.create_all(rt.sql_engine)


def handle_celery_eagar():
    conf = Config()

    if const.CELERY_ALWAYS_EAGER in conf and conf[const.CELERY_ALWAYS_EAGER] == True:
        # TODO: better way to handle this case is lazy-loading, however, it's 
        # a feature not merged to master branch of cqlegine, would be merged
        # in 0.16.
        _init_db_connection()

handle_celery_eagar()

