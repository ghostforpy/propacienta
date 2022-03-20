from django.conf import settings
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter, SimpleRouter
from drf_yasg import openapi
from rest_framework import permissions
from drf_yasg.views import get_schema_view


from propacienta.users.api.views import UserViewSet



schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Propacienta Info",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="nebozhinskiy@gmail.com"),
        lisence=openapi.License(name="BSD Lisense"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

#router.register("users", UserViewSet)


app_name = "api"
urlpatterns = [
    path("", include("propacienta.users.api.urls")),
    path('', include("medicine_cards.api.urls")),
    path('', include("analisis.api.urls")),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
urlpatterns += router.urls
