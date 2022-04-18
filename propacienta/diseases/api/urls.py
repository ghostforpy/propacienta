from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import (  # ChronicDiseaseCreateListView,; ChronicDiseaseDestoryView,
    AuthRetrieveDischargeEpicrisFilesView,
    AuthRetrieveDischargeEpicrisImageView,
    DischargeEpicrisCreateListView,
    DischargeEpicrisDestoryView,
    DischargeEpicrisFileDeleteView,
    DischargeEpicrisImageDeleteView,
    DiseasesViewSet,
    TransferredDiseaseCreateListView,
    TransferredDiseaseDestoryView,
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


router.register("diseases", DiseasesViewSet, basename="diseases")

urlpatterns = [
    path(
        "discharge-epicris-images/<int:pk>/",
        DischargeEpicrisImageDeleteView.as_view(),
        name="discharge-epicris-images-delete",
    ),
    path(
        "discharge-epicris-files/<int:pk>/",
        DischargeEpicrisFileDeleteView.as_view(),
        name="discharge-epicris-files-delete",
    ),
    path(
        "transferred-diseases/<int:pacient_id>/",
        TransferredDiseaseCreateListView.as_view(),
    ),
    path(
        "transferred-diseases-delete/<int:pacient_id>/<int:transferred_disease_id>/",
        TransferredDiseaseDestoryView.as_view(),
    ),
    # path(
    #    'chronic-diseases/<int:pacient_id>/',
    #    ChronicDiseaseCreateListView.as_view()
    # ),
    # path(
    #     'chronic-diseases-delete/<int:pacient_id>/<int:chronic_disease_id>/',
    #     ChronicDiseaseDestoryView.as_view()
    # ),
    path(
        "chronic-diseases-epicrisis/<int:pacient_id>/<int:disease_id>/",
        DischargeEpicrisCreateListView.as_view(),
    ),
    path(
        "chronic-diseases-epicrisis-delete/<int:pacient_id>/<int:discharge_epicris_id>/",
        DischargeEpicrisDestoryView.as_view(),
    ),
    path(
        "auth-request-discharge_epicrisis-files/",
        AuthRetrieveDischargeEpicrisFilesView.as_view(),
    ),
    path(
        "auth-request-discharge_epicrisis-images/",
        AuthRetrieveDischargeEpicrisImageView.as_view(),
    ),
    path("", include(router.urls)),
]
