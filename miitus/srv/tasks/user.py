from __future__ import absolute_import
from celery import shared_task
from ..exceptions import AlreadyExists, DBGenericError, NotExists
from ..models import User
from ..utils import return_exception


@shared_task
@return_exception
def create_new_user(email, password, gender, loc, bday, joinTime):
    """
    ret: None
    """
    # check if this email is registered
    if User.objects(email=email).first():
        raise AlreadyExists('The email is registered: ' + str(email))

    # TODO: "IF NOT EXIST" for insert statement
    User.create(
        email=email,
        password=password,
        gender=gender,
        bDay=bday,
        nation=loc,
        joinTime=joinTime
    )

    # query this user back, and check if password part is the same
    u_back = User.objects(email=email).first()
    if not u_back:
        # cassandra didn't insert our object
        raise DBGenericError('Cassandra did not insert our object: ' + str(email))
    elif u_back.password != password:
        # someone else take this user before this operation.
        raise AlreadyExists('The email is just registered: ' + str(email))


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

