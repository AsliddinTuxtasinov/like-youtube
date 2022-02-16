from django.contrib import admin

from content.models import VideoContent


@admin.register(VideoContent)
class VideoContentAdmin(admin.ModelAdmin):
    pass
