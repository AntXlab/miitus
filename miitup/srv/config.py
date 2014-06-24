import miitup.defs

# celery
CELERY_BROKER_URL = 'amqp://'
CELERY_BACKEND_URL = 'amqp://'

# cqlengine 
CQLENGINE_HOSTS = ['127.0.0.1']

# tornado
# TODO: separate config
from .util import get_static_folder
TORNADO_debug = True
TORNADO_static_path = get_static_folder()
TORNADO_static_url_prefix = miitup.defs.STATIC_URL_PREFIX 

