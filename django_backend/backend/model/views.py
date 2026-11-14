from django.shortcuts import render
from .models import ImageModelRequest
from rest_framework.decorators import api_view
from . import serializers
from rest_framework.response import Response

@api_view(["POST"])
def send_image_to_cnn(request):
  data = serializers.ImageRequestSerializer(data=request.data)
  if data.is_valid():
    data.data.get("image")
    return Response({"message": "complete"})
