from rest_framework import permissions, generics, viewsets, status, validators
from rest_framework.response import Response
from rest_framework.views import APIView

from auser.models import CustomUserChannel
from content.models import VideoContent, Comment, ViewLikeDislike
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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.video_content_ldv_user.add_views(user=request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


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


class LikesView(APIView):
    queryset = VideoContent

    def post(self, request, video_content_id):
        video_content = self.queryset.objects.get(id=video_content_id)
        serializer = VideoContentSerializer(video_content, context={'request': request})

        if ViewLikeDislike.objects.filter(video_content=video_content).exists():
            view_like_dislike = ViewLikeDislike.objects.get(video_content=video_content)
            view_like_dislike.add_likes(user=request.user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        raise validators.ValidationError(
            detail={"message": "you can not like this content or already liked"}, code=status.HTTP_400_BAD_REQUEST)


class DislikeView(APIView):
    queryset = VideoContent

    def post(self, request, video_content_id):
        video_content = self.queryset.objects.get(id=video_content_id)
        serializer = VideoContentSerializer(video_content, context={'request': request})

        if ViewLikeDislike.objects.filter(video_content=video_content).exists():
            view_like_dislike = ViewLikeDislike.objects.get(video_content=video_content)
            view_like_dislike.add_dislikes(user=request.user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        raise validators.ValidationError(
            detail={"message": "you can not dislike this content or already disliked"}, code=status.HTTP_400_BAD_REQUEST)
