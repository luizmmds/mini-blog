from flask import request, Response, json
from neomodel.exception import UniqueProperty
from flask.ext.classy import FlaskView, route
from app.exceptions import BaseException

from .models import User
from .serializers import UserSerializer

class UserAPIView(FlaskView):
    route_base = 'user/'

    def post(self):
        data = request.get_json().copy()
        user = User(**data)
        user.set_password(data.get('password'))
        try:
            user.save()
        except UniqueProperty:
            raise BaseException("Email already exists!", 401)
        return Response("User created!")
        

    @route('login/', methods=['POST'])
    def login(self):
        data = request.get_json()
        user = User.authenticate(data.get('email'), data.get('password'))
        serializer = UserSerializer(user)
        return Response(serializer.data, 200, headers={'Authorization': user.token[0][0].code})
