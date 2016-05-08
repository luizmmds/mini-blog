import uuid
from hashlib import sha224
from neomodel import (StructuredNode, StringProperty, RelationshipTo, RelationshipFrom)

class Token(StructuredNode):
    code = StringProperty()

    def generate_code(self):
        self.code = str(uuid.uuid4())

class User(StructuredNode):
    first_name = StringProperty(required=True)
    last_name = StringProperty(required=True)
    email = StringProperty(unique_index=True)
    password = StringProperty()
    token = RelationshipTo('Token', 'HAS_TOKEN')

    def set_password(self, password):
        self.password = sha224(password.encode('utf-8')).hexdigest()

    @classmethod
    def authenticate(cls, email, password):
        try:
            cls = cls.nodes.get(email=email, password=sha224(password.encode('utf-8')).hexdigest())
            token = Token()
            token.generate_code()
            token.save()
            cls.token.connect(token)
            return cls
        except User.DoesNotExist:
            return False