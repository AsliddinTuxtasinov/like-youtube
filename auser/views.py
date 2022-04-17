from rest_framework import status, validators
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from auser.models import CustomUserChannel, FollowChannel
from auser.serializers import CustomUserChannelSerializer


class CustomUserChannelView(APIView):

    def get(self, request, id):
        queryset = get_object_or_404(CustomUserChannel, id=id)
        serializer = CustomUserChannelSerializer(queryset, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        queryset = get_object_or_404(CustomUserChannel, id=id)

        if queryset.owner == request.user:
            queryset.delete()
        else:
            raise validators.ValidationError(
                detail={"message": "You cannot delete this channel"}, code=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, id):
        queryset = get_object_or_404(CustomUserChannel, id=id)
        serializer = CustomUserChannelSerializer(
            instance=queryset, data=request.data, partial=True)

        if serializer.is_valid():
            if queryset.owner == request.user:
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                raise validators.ValidationError(
                    detail={"message": "You cannot update this channel"}, code=status.HTTP_400_BAD_REQUEST)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserChannelCreateView(APIView):

    def get(self, request):
        queryset = CustomUserChannel.objects.all()
        serializer = CustomUserChannelSerializer(queryset, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = CustomUserChannelSerializer(data=data, context={'request': request})

        if serializer.is_valid():
            owner_id = request.user.id
            qs = CustomUserChannel.objects.filter(owner__id=owner_id)
            if not qs.exists():
                serializer.save(owner_id=owner_id)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            raise validators.ValidationError(
                detail={"message": "You were already created channel"}, code=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowChannelView(APIView):

    def post(self, request, channel_id):

        if FollowChannel.objects.filter(follow_user=request.user).exists():
            channel = get_object_or_404(CustomUserChannel, id=channel_id)
            follow = get_object_or_404(FollowChannel, follow_user=request.user)
            follow.add_follow(channel)

            serializer = CustomUserChannelSerializer(channel, context={'request': request})
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        raise validators.ValidationError(
            detail={"message": "you can not follow, please connect support"}, code=status.HTTP_400_BAD_REQUEST)


class UnFollowChannelView(APIView):

    def post(self, request, channel_id):

        if FollowChannel.objects.filter(follow_user=request.user).exists():
            channel = get_object_or_404(CustomUserChannel, id=channel_id)
            follow = get_object_or_404(FollowChannel, follow_user=request.user)
            follow.remove_follow(channel)

            serializer = CustomUserChannelSerializer(channel, context={'request': request})
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        raise validators.ValidationError(
            detail={"message": "you can not unfollow, please connect support"}, code=status.HTTP_400_BAD_REQUEST)
