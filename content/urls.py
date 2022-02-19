from rest_framework.routers import SimpleRouter
from django.urls import path
from content import views

app_name = 'content'

routers = SimpleRouter()
routers.register(r'', views.VideoContentView, basename='content')

urlpatterns = [
    path('comment/<int:content_pk>/', views.CommentCreateView.as_view(), name='comment-create'),
    path('comment/detail/<int:comment_pk>/', views.CommentDetailView.as_view(), name='comment-detail')
]

urlpatterns += routers.urls
