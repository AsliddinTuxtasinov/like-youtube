from rest_framework.routers import SimpleRouter
from content import views

routers = SimpleRouter()
routers.register(r'', views.VideoContentView, basename='content')

urlpatterns = routers.urls
