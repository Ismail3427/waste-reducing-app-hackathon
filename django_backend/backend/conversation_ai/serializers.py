from rest_framework import serializers

class CreateConversationSerializer(serializers.Serializer):
  userId = serializers.CharField()
  content = serializers.CharField(allow_null=False)
  role = serializers.CharField()
  