from cqlengine.management import delete_keyspace
from miitus.srv.core import Core
from miitus import defs

if __name__ == '__main__':
    c = Core()
    delete_keyspace(defs.CQL_KEYSPACE_NAME)

