from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import PacientViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("pacients", PacientViewSet, basename="pacients")

app_name = "pacients"

urlpatterns = [
    path("", include(router.urls)),
]
