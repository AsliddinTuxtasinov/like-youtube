from django.contrib import admin
from django.contrib.auth import get_user_model, admin as u_admin

from auser.models import CustomUserChannel, FollowChannel
User = get_user_model()


@admin.register(User)
class UserAdmin(u_admin.UserAdmin):
    pass


@admin.register(CustomUserChannel)
class CustomUserChannelAdmin(admin.ModelAdmin):
    pass


@admin.register(FollowChannel)
class FollowChannelAdmin(admin.ModelAdmin):
    pass
