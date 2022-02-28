from django.db.models.signals import post_save
from django.dispatch import receiver

from content.models import VideoContent, ViewLikeDislike


@receiver(post_save, sender=VideoContent)
def create_view_like_dislike(sender, instance, created, **kwargs):
    if created:
        if not ViewLikeDislike.objects.filter(video_content=instance).exists():
            obj = ViewLikeDislike(video_content=instance)
            user = instance.owner_channel.owner
            obj.save()
            obj.add_views(user)
