from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.urls import path, include
from .views import login_view, logout_view


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# router.register("users", UserViewSet, basename="users")
app_name = "auth"
urlpatterns = [
    path("login/", login_view),
    path("logout/", logout_view),
]
