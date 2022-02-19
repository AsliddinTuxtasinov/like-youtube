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
        return str(self.pk)


class Comment(models.Model):
    video_content = models.ForeignKey(to=VideoContent, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    class Meta:
        ordering = ('-created_at',)

    def children(self):  # replies
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

    def __str__(self):
        return str(self.pk)
