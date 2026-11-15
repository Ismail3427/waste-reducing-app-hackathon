from rest_framework import serializers

class CreateUserSerializer(serializers.Serializer):
  name = serializers.CharField()
  email = serializers.CharField()
  userId = serializers.CharField()
