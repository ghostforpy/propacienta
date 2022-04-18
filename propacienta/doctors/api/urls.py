from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import DoctorViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("doctors", DoctorViewSet, basename="doctors")

app_name = "doctors"

urlpatterns = [
    path("", include(router.urls)),
]
