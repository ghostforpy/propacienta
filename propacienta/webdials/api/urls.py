from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import CoturnViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


router.register("coturn", CoturnViewSet, basename="coturn")
# router.register("workdays", WorkDayViewSet, basename="workdays")

urlpatterns = [
    # path(
    #     "get-coturn-credentials/",
    #     TransferredOperationImageDeleteView.as_view(),
    #     name="get-coturn-credentials",
    # ),

    path("", include(router.urls)),
]
