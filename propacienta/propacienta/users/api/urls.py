from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.urls import path, include
from .views import UserViewSet


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# router.register("users", UserViewSet, basename="users")

app_name = "users"

urlpatterns = [
    # path("", include(router.urls)),
    path("", include("djoser.urls")),
]
