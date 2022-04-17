from rest_framework.routers import SimpleRouter
from django.urls import path
from content import views

app_name = 'content'

routers = SimpleRouter()
routers.register(r'', views.VideoContentView, basename='content')

urlpatterns = [
    path('like/<int:video_content_id>/', views.LikesView.as_view(), name='like'),
    path('dislike/<int:video_content_id>/', views.DislikeView.as_view(), name='dislike'),
    path('comment/<int:content_pk>/', views.CommentCreateView.as_view(), name='comment-create'),
    path('comment/detail/<int:comment_pk>/', views.CommentDetailView.as_view(), name='comment-detail')
]

urlpatterns += routers.urls
