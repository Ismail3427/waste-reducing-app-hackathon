from rest_framework import serializers
from .models import ImageModelRequest

class ImageRequestSerializer(serializers.ModelField):
  class Meta:
    model = ImageModelRequest
    fields = ["id", "image", "message"]
    