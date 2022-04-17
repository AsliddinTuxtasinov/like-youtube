from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('auser.urls')),
    path('content/', include('content.urls')),

    # path('api-auth/', include('rest_framework.urls')),
]
urlpatterns += doc_urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
