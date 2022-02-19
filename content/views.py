from rest_framework import permissions, generics, viewsets

from auser.models import CustomUserChannel
from content.models import VideoContent, Comment
from content.serializers import CommentSerializer, VideoContentSerializer


class IsChannelOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        safe_methods = ('PUT', 'PATCH', 'DELETE')
        if request.method in safe_methods:
            return obj.owner_channel == request.user.channel_user
        else:
            return True


class IsCommentOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        safe_methods = ('PUT', 'PATCH', 'DELETE')
        if request.method in safe_methods:
            return obj.author == request.user
        else:
            return True


class VideoContentView(viewsets.ModelViewSet):
    serializer_class = VideoContentSerializer
    queryset = VideoContent.objects.all()
    permission_classes = [IsChannelOwner, permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        channel_id = generics.get_object_or_404(CustomUserChannel, owner=self.request.user).id
        serializer.save(owner_channel_id=channel_id)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class CommentCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.filter(parent=None)
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'content_pk'

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            video_content=generics.get_object_or_404(VideoContent, id=self.kwargs['content_pk'])
        )


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsCommentOwner, permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'comment_pk'
