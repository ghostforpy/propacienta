from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import CoturnViewSet, DialsViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


router.register("coturn", CoturnViewSet, basename="coturn")
router.register("webdials", DialsViewSet, basename="webdials")

urlpatterns = [
    path("", include(router.urls)),
]
