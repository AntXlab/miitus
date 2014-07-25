from __future__ import absolute_import
from celery import shared_task
from ..utils import session_scope
from ..core import Runtime
from ..models.sql import User


rt = Runtime()


@shared_task
def create_new_user(usr_obj):
    """
    ret: None
    """
    global rt 

    with session_scope(rt.sql_session) as s:
        s.add(User(**usr_obj))

    # TODO: once successed, create a real referenced model in cassandra.


@shared_task
def check_user_password(email, password):
    """
    check password, note that the password should be hashed.

    ret: user object if password is correct.
    """
    raise NotImplementedError()

