from __future__ import absolute_import
from werkzeug.utils import find_modules, import_string
from celery import shared_task
from cqlengine import Model
from cqlengine.management import sync_table, create_keyspace
from cqlengine.models import ModelMetaClass
from miitus import defs



@shared_task(time_limit=150)
def prepare_db():
    """
    """
    global c

    # init keyspace
    # TODO: replication-factor:1 is just a dev config
    create_keyspace(defs.CQL_KEYSPACE_NAME, replication_factor=1)

    # sync table
    for name in find_modules(defs.MODEL_PACKAGE_ROOT, recursive=True):
        mod = import_string(name)
        for item_name in dir(mod):
            item = getattr(mod, item_name)
            if type(item) == ModelMetaClass and issubclass(item, Model) and item.__name__ != 'Model':
                sync_table(item)

