from django.contrib.auth import get_user_model
from rest_framework import serializers
from dj_rest_auth.serializers import LoginSerializer, UserDetailsSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account import app_settings as allauth_settings
from allauth.utils import get_username_max_length
from rest_framework.fields import SerializerMethodField

from auser.models import CustomUserChannel, FollowChannel
UserModel = get_user_model()


class LoginCustomSerializer(LoginSerializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})


class RegisterCustomSerializer(RegisterSerializer):
    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_settings.USERNAME_MIN_LENGTH,
        required=allauth_settings.USERNAME_REQUIRED,
    )
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'first_name': self.validated_data.get('username', ''),
            'last_name': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }


class CustomUserChannelSerializer(serializers.ModelSerializer):
    owner = SerializerMethodField()
    create_at = serializers.DateTimeField(read_only=True)

    follow_channel_url = serializers.HyperlinkedIdentityField(
        view_name='follow-channel',
        read_only=True,
        lookup_field='pk',
        lookup_url_kwarg='channel_id'
    )
    unfollow_channel_url = serializers.HyperlinkedIdentityField(
        view_name='unfollow-channel',
        read_only=True,
        lookup_field='pk',
        lookup_url_kwarg='channel_id'
    )

    class Meta:
        model = CustomUserChannel
        fields = ("id", "owner", "name", "describe", "create_at", "owner_id", "follow_channel_url", "unfollow_channel_url")

    def get_owner(self, obj):
        return obj.owner.username


class FollowChannelSerializer(serializers.ModelSerializer):
    following_channels = SerializerMethodField()

    class Meta:
        model = FollowChannel
        fields = ['id', 'follow_user', 'following_channels']

    def get_following_channels(self, obj):
        qs = obj.follow_channels.all()
        return CustomUserChannelSerializer(qs, many=True, context={'request': self.context.get('request')}).data


class UserDetailsCustomSerializer(UserDetailsSerializer):
    your_channel = SerializerMethodField()
    following_channels = SerializerMethodField()

    class Meta:
        model = UserModel
        extra_fields = ['date_joined', 'your_channel', 'following_channels']

        if hasattr(UserModel, 'USERNAME_FIELD'):
            extra_fields.append(UserModel.USERNAME_FIELD)
        if hasattr(UserModel, 'EMAIL_FIELD'):
            extra_fields.append(UserModel.EMAIL_FIELD)
        if hasattr(UserModel, 'first_name'):
            extra_fields.append('first_name')
        if hasattr(UserModel, 'last_name'):
            extra_fields.append('last_name')

        fields = ('id', *extra_fields)
        read_only_fields = ('email', 'date_joined')

    def get_following_channels(self, obj):
        if FollowChannel.objects.filter(follow_user=obj).exists():
            follow_qs = FollowChannel.objects.get(follow_user=obj)
            return FollowChannelSerializer(follow_qs).data
        return None

    def get_your_channel(self, obj):
        if CustomUserChannel.objects.filter(owner=obj).exists():
            channel_qs = CustomUserChannel.objects.get(owner=obj)
            return CustomUserChannelSerializer(channel_qs, context={'request': self.context.get('request')}).data
        return None
