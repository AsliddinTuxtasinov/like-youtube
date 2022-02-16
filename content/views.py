from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from auser.models import CustomUserChannel
from content.models import VideoContent
from content.serializers import VideoContentSerializer


class IsChannelOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        safe_methods = ('PUT', 'PATCH', 'DELETE')
        if request.method in safe_methods:
            return obj.owner_channel == request.user.channel_user
        else:
            return True


class VideoContentView(ModelViewSet):
    serializer_class = VideoContentSerializer
    queryset = VideoContent.objects.all()
    permission_classes = [IsChannelOwner, permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        channel_id = get_object_or_404(CustomUserChannel, owner=self.request.user).id
        serializer.save(owner_channel_id=channel_id)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
