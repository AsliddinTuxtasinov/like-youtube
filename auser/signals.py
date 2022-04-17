from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from auser.models import CustomUserChannel, FollowChannel
User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if not CustomUserChannel.objects.filter(owner=instance).exists():
            channel = CustomUserChannel(owner=instance)
            channel.name = instance.get_full_name()
            channel.save()

        if not FollowChannel.objects.filter(follow_user=instance).exists():
            follow = FollowChannel(follow_user=instance)
            follow.save()
