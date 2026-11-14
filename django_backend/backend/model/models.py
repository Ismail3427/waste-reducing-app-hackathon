import uuid
from django.db import models

class ImageModelRequest(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  image = models.ImageField(upload_to='images/')
  message = models.CharField(max_length=255)
  