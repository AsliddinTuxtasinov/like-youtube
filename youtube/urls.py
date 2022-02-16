from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('auser.urls')),
    path('content/', include('content.urls')),


    path('api-auth/', include('rest_framework.urls')),
]
