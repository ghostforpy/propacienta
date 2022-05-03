from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import DoctorSpecializationViewSet, DoctorViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("doctors", DoctorViewSet, basename="doctors")
router.register(
    "doctors-specializations",
    DoctorSpecializationViewSet,
    basename="doctors-specializations",
)

app_name = "doctors"

urlpatterns = [
    path("", include(router.urls)),
]
