from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import DialogMessageViewSet, DialogViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


router.register(
    "dialogs",
    DialogViewSet,
    basename="dialogs"
)
router.register(
    "dialog-messages",
    DialogMessageViewSet,
    basename="dialog-messages"
)

urlpatterns = [
    path("", include(router.urls)),
]
