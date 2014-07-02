from miitus import defs

# celery
CELERY_MAIN_NAME = 'mittus.srv.tasks'
CELERY_BROKER_URL = 'amqp://'
CELERY_BACKEND_URL = 'amqp://'
CELERY_MODULES_INCLUDE = [
]

# cqlengine 
CQLENGINE_HOSTS = ['127.0.0.1']

# tornado
# TODO: separate config
from .util import get_static_folder
TORNADO_debug = True
TORNADO_static_path = get_static_folder()
TORNADO_static_url_prefix = defs.STATIC_URL_PREFIX 
TORNADO_xsrf_cookie = True
TORNADO_2PATCH__cookie_secret = '__SOMETHING_RANDOM__'

# TODO: this part should be patched before deployment
# security
_2PATCH_TOKEN_SECRET_KEY = '__SOMETHING_RANDOM__'
_2PATCH_HASH_SECRET_KEY = '__SOMETHING_RANDOM__'


