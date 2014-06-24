from __future__ import absolute_import
from cqlengine import Model, columns, uuid4

class User(Model):
    """
    class User

    only kept static information here. For dynamic info, ex. last-login,
    we would kept them in other table
    """
    id = columns.UUID(primary_key=True, default=uuid4)

    email = columns.Text(max_length=255, required=True)
    password = columns.Bytes(required=True)
    gender = columns.Integer()
    bDay = columns.Date()
    nation = columns.Integer()

    # TODO: other static use another model?
    joinTime = columns.DateTime()

    def get_auth_token(self):
        return login_serializer.dumps(self.email, self.password)

