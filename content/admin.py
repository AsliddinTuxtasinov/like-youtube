from django.contrib import admin

from content.models import VideoContent, VideoProxy, Comment, ViewLikeDislike


@admin.register(VideoContent)
class VideoContentAdmin(admin.ModelAdmin):
    readonly_fields = ('views_count', 'likes_count',  'dislikes_count')


@admin.register(VideoProxy)
class VideoProxyAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ('is_parent',)


@admin.register(ViewLikeDislike)
class ViewLikeDislikeAdmin(admin.ModelAdmin):
    # readonly_fields = ('is_parent',)
    pass
