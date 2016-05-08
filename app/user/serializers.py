from app.serializers import ModelSerializer

class UserSerializer(ModelSerializer):
    fields = ('first_name', 'last_name', 'email')