from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import WorkDaySlotsViewSet, WorkDayViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


router.register("freetimeslots", WorkDaySlotsViewSet, basename="freetimeslots")
router.register("workdays", WorkDayViewSet, basename="workdays")

urlpatterns = [
    # path(
    #     "transferred-operation-images/<int:pk>/",
    #     TransferredOperationImageDeleteView.as_view(),
    #     name="transferred-operation-images-delete",
    # ),
    # path(
    #     "transferred-operation-files/<int:pk>/",
    #     TransferredOperationFileDeleteView.as_view(),
    #     name="transferred-operation-files-delete",
    # ),
    # path(
    #     "transferred-operations/<int:pacient_id>/",
    #     TransferredOperationCreateListView.as_view(),
    # ),
    # path(
    #     "transferred-operation-delete/<int:pacient_id>/<int:transferred_operation_id>/",
    #     TransferredOperationDestoryView.as_view(),
    # ),
    # path(
    #     "auth-request-transferred_operation-files/",
    #     AuthRetrieveTransferredOperationFileView.as_view(),
    # ),
    # path(
    #     "auth-request-transferred_operation-images/",
    #     AuthRetrieveTransferredOperationImageView.as_view(),
    # ),
    path("", include(router.urls)),
]
