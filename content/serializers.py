from django.contrib.auth import get_user_model
from rest_framework import serializers

from auser.serializers import CustomUserChannelSerializer
from content.models import VideoContent
User = get_user_model()


class VideoContentSerializer(serializers.ModelSerializer):
    owner_channel = CustomUserChannelSerializer(read_only=True)
    create_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = VideoContent
        fields = ['id', 'owner_channel', 'title', 'create_at', 'owner_channel_id']
