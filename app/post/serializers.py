from app.serializers import ModelSerializer

class PostSerializer(ModelSerializer):
    fields = ('title', 'content', 'created_at')