from django.shortcuts import render
from . import models
from rest_framework.decorators import api_view
from . import serializers
from backend.user.models import User
import ollama
from rest_framework.response import Response


@api_view(["POST"])
def create_conversation(request):
    data = serializers.CreateConversationSerializer(data=request.data)

    if data.is_valid():
        clean_data = data.validated_data
        user = User.objects.get(userId=clean_data.get("userId"))

        conversation = models.Conversation.objects.create(user=user)
        models.Message.objects.create(
            conversation=conversation,
            role=clean_data.get("role"),
            content=clean_data.get("content"),
        )

        response = ollama.chat(
            model="llama3.2",
            messages=list(conversation.thread.all().values("role", "content")),
        )
        reply = response.message.content
        models.Message.objects.create(
            conversation=conversation, role="system", content=reply
        )
        return Response({"message": reply})


@api_view(["POST"])
def continue_conversation(request):
    data = serializers.ContinueConversationSerializer(data=request.data)
    if data.is_valid():
        clean_data = data.validated_data
        user = User.objects.get(userId=clean_data.get("userId"))

        conversation = models.Conversation.objects.get(
            id=clean_data.get("conversationId")
        )
        if user.id != conversation.user.id:
            return Response({"message": "Wrong user"})

        models.Message.objects.create(
            conversation=conversation,
            role=clean_data.get("role"),
            content=clean_data.get("content"),
        )

        response = ollama.chat(
            model="llama3.2",
            messages=list(conversation.thread.all().values("role", "content")),
        )

        reply = response.message.content

        models.Message.objects.create(
            conversation=conversation, role="system", content=reply
        )
        return Response({"response": reply})
