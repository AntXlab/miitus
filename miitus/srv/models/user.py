from __future__ import absolute_import
from cqlengine import Model, columns, exceptions
from validate_email import validate_email
from ..core import Core
import uuid


c = Core()

class User(Model):
    """
    class User

    only kept static information here. For dynamic info, ex. last-login,
    we would kept them in other table
    """
    id = columns.UUID(primary_key=True, default=uuid.uuid4)

    email = columns.Text(max_length=255, required=True)
    password = columns.Bytes(required=True)
    gender = columns.Integer()
    bDay = columns.Date()
    nation = columns.Integer()

    # TODO: other static use another model?
    joinTime = columns.DateTime()

    def validate(self):
        super(User, self).validate()

        if not validate_email(self.email):
            raise exceptions.ValidationError('Invalid email:' + self.email)

        if self.gender < 1 or self.gender > 4:
            raise exceptions.ValidationError('Invalid gender:' + str(self.gender))

    def get_auth_token(self):
        return c.serializer.dumps(self.email, self.password)

