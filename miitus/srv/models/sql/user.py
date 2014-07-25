from __future__ import absolute_import
from validate_email import validate_email
from sqlalchemy import Sequence, Column, Integer, String, TEXT
from sqlalchemy.orm import validates
from ...prep import Preparation
from ...utils import SQLHelperMixin


prep = Preparation()


class User(prep.Base, SQLHelperMixin):
    """
    class User

    only kept static information here. For dynamic info, ex. last-login,
    we would kept them in other table
    """

    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    email = Column(String(255), unique=True)
    password = Column(TEXT())

    @validates('email')
    def validate_email(self, key, email):
        if not validate_email(email):
            raise ValueError('Invalid email:' + email)

        return email

