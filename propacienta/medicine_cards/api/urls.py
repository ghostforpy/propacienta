from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import (
    IndependentResearchViewSet,
    MedicineCardViewSet,
    ResultIndependentResearchCreateList,
    ResultIndependentResearchDestory,
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


router.register('medicine-cards', MedicineCardViewSet, basename='medicine-cards')
router.register('independent-researchs',
                IndependentResearchViewSet,
                basename='independent-researchs')
app_name = "medicine-cards"

urlpatterns = [
    path(
        'independent-research-results/<int:pacient_id>/<int:independent_research_id>/',
        ResultIndependentResearchCreateList.as_view()
    ),
    path(
        'independent-research-results/<int:pacient_id>/<int:independent_research_id>/<int:independent_research_result_id>/',
        ResultIndependentResearchDestory.as_view()
    ),
    path('', include(router.urls)),
]
