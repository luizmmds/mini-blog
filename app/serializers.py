from flask import json, make_response

class ModelSerializer():
    many = False
    fields = ('id',)
    relations = {}
    data = []

    def __init__(self, instance, many=False):
        self.fields += ('id', 'is_active', 'created_at')
        if many:
            serializer = []
            for inst in instance:
                serializer.append(self.to_representation(inst))
        else:
            serializer = self.to_representation(instance)

        self.data = json.dumps(serializer)

    def to_representation(self, instance):
        serializer = {}
        for field in self.fields:
            if hasattr(instance, field):
                serializer.update( { field: getattr(instance, field)} )
        return serializer
