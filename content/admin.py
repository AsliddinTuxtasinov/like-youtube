from django.contrib import admin

from content.models import VideoContent, Comment


@admin.register(VideoContent)
class VideoContentAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ('is_parent',)
