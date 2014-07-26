from __future__ import absolute_import
from celery import shared_task
from ..utils import session_scope
from ..core import Runtime
from ..models import sql, cql


rt = Runtime()


@shared_task
def create_new_user(usr_obj):
    """
    ret: None
    """
    global rt 

    # insert into sql to make sure uniqueness
    u = sql.User(**usr_obj)
    with session_scope(rt.sql_session, expire=False) as s:
        s.add(u)

    # update return value
    usr_obj.update(id=u.id)

    # duplicate a record in cassandra
    cql.User.create(**usr_obj)

    return usr_obj

@shared_task
def check_user_password(email, password):
    """
    check password, note that the password should be hashed.

    ret: user object if password is correct.
    """
    global rt

    raise NotImplementedError()

