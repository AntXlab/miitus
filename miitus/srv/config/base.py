# celery
CELERY_MAIN_NAME = 'mittus.srv.tasks'
CELERY_BROKER_URL = 'amqp://'
CELERY_BACKEND_URL = 'amqp://'
CELERY_CONF_CELERY_IMPORTS = [
]
CELERY_CONF_CELERY_CHORD_PROPAGATES = True

# cqlengine 
CQLENGINE_HOSTS = ['127.0.0.1']
CQL_SHORT_TTL = 16

# sqlalchemy
SQLALCHEMY_URL = 'sqlite:///test.db'
SQLALCHEMY_ECHO = True

# tornado
TORNADO_xsrf_cookie = True

# security
MAX_AGE = 21
USER_COOKIE_DURATION = 3
TOKEN_COOKIE_DURATION = 14
