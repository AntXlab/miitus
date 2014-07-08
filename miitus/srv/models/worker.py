from __future__ import absolute_import
from cqlengine import Model, columns


class Worker(Model):
    """
    class Worker

    let each worker has an distributed unique id.
    """
    id = columns.Integer(primary_key=True)
    salt = columns.BigInt(required=True)
