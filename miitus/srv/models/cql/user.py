from __future__ import absolute_import
from cqlengine import Model, columns
from cqlengine import exceptions
from validate_email import validate_email
from ...utils import CQLHelperMixin


class User(Model, CQLHelperMixin):
    """
    class User

    only kept static information here. For dynamic info, ex. last-login,
    we would kept them in other table
    """
    id = columns.Integer(primary_key=True)
    email = columns.Text(max_length=255, required=True, index=True)
    password = columns.Text(required=True)
    gender = columns.Integer(default=0)
    b_day = columns.Date()
    nation = columns.Integer()

    # other static use another model?
    join_time = columns.DateTime()

    def validate(self):
        super(User, self).validate()

        if not validate_email(self.email):
            raise exceptions.ValidationError('Invalid email:' + self.email)

        if self.gender > 4:
            raise exceptions.ValidationError('Invalid gender:' + str(self.gender))

