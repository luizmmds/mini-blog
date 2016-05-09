import uuid
from hashlib import sha224
from app.exceptions import BaseException
from neomodel import (StructuredNode, StringProperty, RelationshipTo, One, db)

def get_by_id(cls, id):
    results, columns = db.cypher_query("START a=node({self}) MATCH a RETURN a", {'self': cls.__name__})
    return [cls.inflate(row[0]) for row in results]

class Token(StructuredNode):
    code = StringProperty()
    user = RelationshipTo('User', 'BELONGS_TO_USER', cardinality=One)

    def generate_code(self):
        self.code = str(uuid.uuid4())

class User(StructuredNode):
    first_name = StringProperty(required=True)
    last_name = StringProperty(required=True)
    email = StringProperty(unique_index=True)
    password = StringProperty()
    token = RelationshipTo('Token', 'HAS_TOKEN')

    def posts(self):
        from app.post.models import Post
        results, columns = self.cypher("MATCH (user:User)<-[:POSTED]->(post:Post) RETURN post")
        return [Post.inflate(row[0]) for row in results]

    def set_password(self, password):
        self.password = sha224(password.encode('utf-8')).hexdigest()

    @classmethod
    def get_by_id(cls, id):
        results, columns = db.cypher_query("START a=node({self}) MATCH a RETURN a", {'self': cls.__name__})
        import code; code.interact(local=locals())
        if len(results):
            return [cls.inflate(row[0]) for row in results][0]
        else:
            raise BaseException('User not found', 400)


    @classmethod
    def authenticate(cls, email, password):
        try:
            cls = cls.nodes.get(email=email, password=sha224(password.encode('utf-8')).hexdigest())
        except User.DoesNotExist:
            return False
        token = Token()
        token.generate_code()
        token.save()
        token.user.connect(cls)
        cls.token.connect(token)
        return cls