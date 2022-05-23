from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import AppointmentOrderDoctorViewSet, AppointmentOrderPacientViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


router.register(
    "pacient-appointments",
    AppointmentOrderPacientViewSet,
    basename="pacient-appointments"
)
router.register(
    "doctor-appointments",
    AppointmentOrderDoctorViewSet,
    basename="doctor-appointments"
)

urlpatterns = [
    # path(
    #     "analysis-results-images/<int:pk>/",
    #     AnalysisResultImageDeleteView.as_view(),
    #     name="analysis-results-images-delete",
    # ),
    # path(
    #     "analysis-results-files/<int:pk>/",
    #     AnalysisResultFileDeleteView.as_view(),
    #     name="analysis-results-files-delete",
    # ),
    # path(
    #     "analysis-results/<int:pacient_id>/<int:analysis_id>/",
    #     AnalysisResultCreateListView.as_view(),
    # ),
    # path(
    #     "analysis-results-delete/<int:pacient_id>/<int:analysis_result_id>/",
    #     AnalysisResultDestoryView.as_view(),
    # ),
    # path(
    #     "auth-request-analisis_results-files/",
    #     AuthRetrieveAnalysisResultsFileView.as_view(),
    # ),
    # path(
    #     "auth-request-analisis_results-images/",
    #     AuthRetrieveAnalysisResultsImageView.as_view(),
    # ),
    path("", include(router.urls)),
]
