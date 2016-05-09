from datetime import datetime
from neomodel import (StructuredNode, StringProperty, RelationshipFrom, DateTimeProperty)
from app.user.models import User

class Post(StructuredNode):
    title = StringProperty()
    content = StringProperty()
    created_at = DateTimeProperty(default=lambda: datetime.now())
    author = RelationshipFrom('User', 'POSTED')

class Comments(StructuredNode):
    pass
