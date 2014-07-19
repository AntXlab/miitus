from __future__ import absolute_import
from celery import shared_task
from ..exceptions import Conflict, NotExists, ParellelInsertionDetected
from ..models import User, EmailLocker
from ..utils import Config
from ..core import Core


c = Core()
conf = Config()


@shared_task
def create_new_user(id, email, password, gender, nation, b_day, joinTime):
    """
    ret: None
    """
    global conf, c

    # check if this email is already registered
    if User.objects(email=email).first():
        raise Conflict()

    # creat locker instance
    salt=c.random()
    locker = EmailLocker(email=email, salt=salt)
 
    # TODO: refine this part when if-not-exist supported
    if EmailLocker.objects(email=email).first():
        raise ParellelInsertionDetected()

    try:
        locker.ttl(conf['CQL_SHORT_TTL']).save()

        # make sure we own the lock
        if EmailLocker.objects(email=email).first().salt != salt:
            raise ParellelInsertionDetected()

        User.create(
            id=id,
            email=email,
            password=password,
            gender=gender,
            b_day=b_day,
            nation=nation,
            joinTime=joinTime
        )
    finally:
        locker.delete()


@shared_task
def check_user_password(email, password):
    """
    check password, note that the password should be hashed.

    ret: user object if password is correct.
    """
    u = User.objects(email=email).first()
    if u:
        return u.password == password
    else:
        raise NotExists()

