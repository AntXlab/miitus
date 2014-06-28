from __future__ import absolute_import
from ..core import Core
from ..models import User


c = Core()


@c.worker.task()
def create_new_user(email, password, gender, loc, bday, joinTime):
    """
    ret: (uid, err)

    err -
    0: success
    1: already_exist
    """
    # check if this email is registered
    q = User.objects(User.email == email)
    u = q.first()
    if u:
        return (None, 1)
    else:
        """
        new_u = User(
            email=email,
            password=password,
            gender=gender,
            bDay=bday,
            nation=loc,
            joinTime=joinTime
        )

        new_u.save()
        """
        return (None, 2)

