from django.urls import path
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        default_version="1.0.0",
        title="Like Youtube",
        description="""
        This project can be an example of an api project, and in the process of creating it, 
        I learned how to work with celery and api. while working with celery I used to create a video proxy in
        this project.""",
        terms_of_service="https://t.me/Tuxtasinov_Asliddin",
        contact=openapi.Contact(email="asliddintukhtasinov5@gmail.com"),
    ),
    public=True,
    permission_classes=(AllowAny,)
)

urlpatterns = [
    path('', schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path('redoc/', schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc-ui"),
]
