import miitus.defs

# celery
CELERY_MAIN_NAME = 'mittus.srv.tasks'
CELERY_BROKER_URL = 'amqp://'
CELERY_BACKEND_URL = 'amqp://'
CELERY_MODULES_INCLUDE = [
    'miitus.srv.tasks.user'
]

# cqlengine 
CQLENGINE_HOSTS = ['127.0.0.1']

# tornado
# TODO: separate config
from .util import get_static_folder
TORNADO_debug = True
TORNADO_static_path = get_static_folder()
TORNADO_static_url_prefix = miitus.defs.STATIC_URL_PREFIX 
TORNADO_xsrf_cookie = True

# TODO: this part should be patched before deployment
# security
_2PATCH_TOKEN_SECRET_KEY = '?\xbf,\xb4\x8d\xa3"<\x9c\xb0@\x0f5\xab,w\xee\x8d$0\x13\x8b83'
_2PATCH_HASH_SECRET_KEY = '?\xbe,\xb3\x8d\xa3"<\x9c\xb0@\x0f5\xab,w\xee\x8d$0\x13\x8b82'

