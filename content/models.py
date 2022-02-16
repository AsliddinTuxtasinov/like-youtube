from django.db import models
from django.contrib.auth import get_user_model

from auser.models import CustomUserChannel
User = get_user_model()


class VideoContent(models.Model):
    owner_channel = models.ForeignKey(to=CustomUserChannel, on_delete=models.CASCADE, related_name="owner_channel")
    title = models.CharField(max_length=255)
    describe = models.TextField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
