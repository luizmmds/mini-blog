from flask import request, Response, json
from flask.ext.classy import FlaskView, route
from app.exceptions import BaseException
from app.user.models import Token, User, get_by_id
from .models import Post
from .serializers import PostSerializer

class PostAPIView(FlaskView):
    route_base = "post/"

    @route('', methods=['GET'])
    def get_all(self):
        try:
            token = Token.nodes.get(code=request.headers.get('Authorization'))
        except Token.DoesNotExist:
            raise BaseException("Invalid Token", 400)

        return Response(PostSerializer(token.user[0][0].posts(), True).data)

    @route('/user/<int:id>/', methods=['GET'])
    def get_by_user(self, id):
        try:
            user = get_by_id(User, id)
        except User.DoesNotExist:
            raise BaseException("User not found", 400)
        import code; code.interact(local=locals())
        return Response(PostSerializer(user.posts(), True).data)

    def post(self):
        data = request.get_json().copy()
        try:
            token = Token.nodes.get(code=request.headers.get('Authorization'))
        except Token.DoesNotExist:
            raise BaseException("Invalid Token", 400)

        post = Post(**data).save()
        post.author.connect(token.user[0][0])
        return Response(PostSerializer(post).data)