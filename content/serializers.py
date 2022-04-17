from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from auser.serializers import CustomUserChannelSerializer
from content.models import VideoContent, Comment, VideoProxy
User = get_user_model()


class CommentChildSerializer(serializers.ModelSerializer):
    author = SerializerMethodField()
    video_content = SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'text', 'video_content', 'author', 'created_at']

    def get_author(self, obj):
        return obj.author.username

    def get_video_content(self, obj):
        return obj.video_content.title


class CommentSerializer(serializers.ModelSerializer):
    author = SerializerMethodField()
    video_content = SerializerMethodField()
    reply_count = SerializerMethodField()
    replies = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'text', 'parent', 'video_content', 'author',
            'reply_count', 'replies', 'created_at'
        ]

    def get_author(self, obj):
        return obj.author.username

    def get_video_content(self, obj):
        return obj.video_content.title

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None


class VideoProxySerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoProxy
        fields = '__all__'


class VideoContentSerializer(serializers.ModelSerializer):
    owner_channel = CustomUserChannelSerializer(read_only=True)
    # proxy_videos = VideoProxySerializer(read_only=True, many=True)
    proxy_videos = serializers.SerializerMethodField()
    comments = SerializerMethodField()

    content_detail_url = serializers.HyperlinkedIdentityField(
        view_name='content:content-detail', read_only=True,
        lookup_field='pk')
    create_comment_url = serializers.HyperlinkedIdentityField(
        view_name='content:comment-create', read_only=True,
        lookup_url_kwarg='content_pk')
    like_url = serializers.HyperlinkedIdentityField(
        view_name='content:like', read_only=True,
        lookup_field='pk', lookup_url_kwarg='video_content_id')
    dislike_url = serializers.HyperlinkedIdentityField(
        view_name='content:dislike', read_only=True,
        lookup_field='pk', lookup_url_kwarg='video_content_id')

    class Meta:
        model = VideoContent
        fields = [
            'content_detail_url', 'like_url', 'dislike_url', 'id', 'title', 'describe',
            'file_video', 'proxy_videos', 'views_count', 'likes_count',  'dislikes_count',
            'owner_channel_id', 'owner_channel', 'comments', 'create_comment_url'
        ]
        read_only_fields = ['create_at']

    def get_comments(self, obj):
        qs = obj.comments.filter(parent=None)
        return CommentSerializer(qs, many=True).data

    def get_proxy_videos(self, obj):
        return VideoProxySerializer(obj.video_proxy, many=True).data
