from django.urls import path, include

from auser import views


urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),

    path('channel/<int:id>/', views.CustomUserChannelView.as_view(), name="channel"),
    path('channel/create/', views.CustomUserChannelCreateView.as_view(), name="channel-create"),
    path('follow/<int:channel_id>/', views.FollowChannelView.as_view(), name="follow-channel"),
    path('unfollow/<int:channel_id>/', views.UnFollowChannelView.as_view(), name="unfollow-channel"),
]
