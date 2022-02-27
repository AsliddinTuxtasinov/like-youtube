from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()


class CustomUserChannel(models.Model):
    owner = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE, related_name="channel_user")
    name = models.CharField(max_length=255, null=True, blank=True)
    describe = models.TextField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.owner.get_full_name()
        super().save(*args, **kwargs)

    def __str__(self):
        # return self.name
        return str(self.pk)


class FollowChannel(models.Model):
    follow_user = models.OneToOneField(
        to=CustomUser, on_delete=models.CASCADE, related_name="follow_user")
    follow_channels = models.ManyToManyField(
        to=CustomUserChannel, related_name="follow_channels", blank=True, null=True)

    def add_follow(self, channel):
        your_channel_id = self.follow_user.channel_user.id
        if (channel.id != your_channel_id) and (channel not in self.follow_channels.all()):
            self.follow_channels.add(channel)

    def remove_follow(self, channel):
        your_channel_id = self.follow_user.channel_user.id
        if (channel.id != your_channel_id) and (channel in self.follow_channels.all()):
            self.follow_channels.remove(channel)

    def __str__(self):
        return f"{self.follow_user}'s following"
