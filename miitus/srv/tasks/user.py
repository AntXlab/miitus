from __future__ import absolute_import
from celery import shared_task
from ..exceptions import AlreadyExists, NotExists, ParellelInsertionDetected
from ..models import User, EmailLocker
from ..utils import return_exception, Config
from ..core import Core


c = Core()
conf = Config()


@shared_task
@return_exception
def create_new_user(id, email, password, gender, loc, bday, joinTime):
    """
    ret: None
    """
    # check if this email is already registered
    if User.objects(email=email).first():
        raise AlreadyExists('The email is registered: ' + str(email))

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
            email=email,
            password=password,
            gender=gender,
            bDay=bday,
            nation=loc,
            joinTime=joinTime
        )
    finally:
        locker.delete()


@shared_task
@return_exception
def check_user_password(email, password):
    """
    check password, note that the password should be hashed.

    ret: True is check passed.
    """
    u = User.objects(email=email).first()
    if u:
        return u.password == password
    else:
        raise NotExists()

