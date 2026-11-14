from django.shortcuts import render
from . import models
from rest_framework.decorators import api_view
from . import serializers
from user.models import User
import ollama
from rest_framework.response import Response


@api_view(["POST"])
def create_conversation(request):
    data = serializers.CreateConversationSerializer(data=request.data)

    if data.is_valid():
        clean_data = data.validated_data
        user = User.objects.get(userId=clean_data.get("userId"))

        message = models.Message.objects.create(
            role=clean_data.get("role"), content=clean_data.get("content")
        )
        message.save()

        conversation = models.Conversation.objects.create(user=user)
        conversation.thread.set([message])
        conversation.save()

        response = ollama.chat(model="llama3.2", messages=conversation.thread.all().values("role", "content"))

        reply = response.message.content
        return Response({"message": reply})
