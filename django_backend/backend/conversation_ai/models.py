from django.db import models
import uuid
from user.models import User

class Message(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  role = models.CharField()
  content = models.CharField()

class Conversation(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  thread = models.ManyToManyField(Message)
  user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name="conversation_user"
  )
