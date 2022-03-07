from django.db import models
from django.contrib.auth import get_user_model

from auser.models import CustomUserChannel
User = get_user_model()


class VideoContent(models.Model):
    owner_channel = models.ForeignKey(to=CustomUserChannel, on_delete=models.CASCADE, related_name="owner_channel")
    title = models.CharField(max_length=255)
    describe = models.TextField(null=True, blank=True)
    file_video = models.FileField(upload_to='videos/')
    create_at = models.DateTimeField(auto_now_add=True)

    @property
    def video_proxy(self):
        return self.video_proxy.all()

    @property
    def views_count(self):
        return self.video_content_ldv_user.views.all().count()

    @property
    def likes_count(self):
        return self.video_content_ldv_user.likes.all().count()

    @property
    def dislikes_count(self):
        return self.video_content_ldv_user.dislikes.all().count()

    def __str__(self):
        return str(self.pk)


class VideoProxy(models.Model):
    original_video = models.ForeignKey(to=VideoContent, on_delete=models.CASCADE, related_name="video_proxy")
    video_proxy = models.FileField(upload_to='videos/')
    size = models.IntegerField()
    frame = models.IntegerField()

    # def __str__(self):
    #     return f"{self.video_proxy}"


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


class ViewLikeDislike(models.Model):
    video_content = models.OneToOneField(
        to=VideoContent, on_delete=models.CASCADE, related_name="video_content_ldv_user")
    likes = models.ManyToManyField(to=User, blank=True, related_name="video_content_like")
    dislikes = models.ManyToManyField(to=User, blank=True, related_name="video_content_dislikes")
    views = models.ManyToManyField(to=User, blank=True, related_name="video_content_views")

    def add_views(self, user):
        if user not in self.views.all():
            self.views.add(user)

    def add_likes(self, user):
        if user not in self.likes.all():
            self.likes.add(user)
        if user in self.dislikes.all():
            self.dislikes.remove(user)

    def add_dislikes(self, user):
        if user not in self.dislikes.all():
            self.dislikes.add(user)
        if user in self.likes.all():
            self.likes.remove(user)

    def __str__(self):
        return f"{self.video_content} | {self.views.count()} | {self.likes.count()} | {self.dislikes.count()}"
