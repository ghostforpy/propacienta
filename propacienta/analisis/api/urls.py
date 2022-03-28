from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.urls import path, include
from .views import (AnalysisViewSet,
                    AnalysisResultCreateListView,
                    AnalysisResultDestoryView,
                    AuthRetrieveAnalysisResultsImageView,
                    AuthRetrieveAnalysisResultsFileView,
                    AnalysisResultImageDeleteView,
                    AnalysisResultFileDeleteView)


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


router.register('analisys', AnalysisViewSet, basename='analisys')
#router.register('independent-researchs', 
#                IndependentResearchViewSet, 
#                basename='independent-researchs')
#router.register('independent-research-results',
#                ResultIndependentResearchViewSet,
#                basename='independent-research-results')
# app_name = "analisys"

urlpatterns = [
    path(
        "analysis-results-images/<int:pk>/",
        AnalysisResultImageDeleteView.as_view(),
        name="analysis-results-images-delete"
    ),
    path(
        "analysis-results-files/<int:pk>/",
        AnalysisResultFileDeleteView.as_view(),
        name="analysis-results-files-delete"
    ),
    path(
       'analysis-results/<int:pacient_id>/<int:analysis_id>/',
       AnalysisResultCreateListView.as_view()
    ),
    path(
        'analysis-results-delete/<int:pacient_id>/<int:analysis_result_id>/',
        AnalysisResultDestoryView.as_view()
    ),
    path(
       'auth-request-analisis_results-files/',
       AuthRetrieveAnalysisResultsFileView.as_view()
    ),
    path(
       'auth-request-analisis_results-images/',
       AuthRetrieveAnalysisResultsImageView.as_view()
    ),
    path('', include(router.urls)),
]
