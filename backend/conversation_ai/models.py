from django.db import models
import uuid
from backend.user.models import User

class Message(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  role = models.CharField()
  content = models.CharField()
  conversation = models.ForeignKey(
    "Conversation",
    on_delete=models.CASCADE,
    related_name="thread",
  )
  
  
class Conversation(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name="conversation_user"
  )
