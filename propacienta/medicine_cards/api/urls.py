from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.urls import path, include
from .views import (MedicineCardViewSet,
                    IndependentResearchViewSet,
                    ResultIndependentResearchList)
                    #ResultIndependentResearchViewSet)


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


router.register('medicine-cards', MedicineCardViewSet, basename='medicine-cards')
router.register('independent-researchs', 
                IndependentResearchViewSet, 
                basename='independent-researchs')
#router.register('independent-research-results',
#                ResultIndependentResearchViewSet,
#                basename='independent-research-results')
app_name = "medicine-cards"

urlpatterns = [
    path(
        'independent-research-results/<int:pacient_id>/<int:independent_research_id>/',
        ResultIndependentResearchList.as_view()
    ),
    path(
        'independent-research-results/<int:pacient_id>/<int:independent_research_id>/<int:independent_research_result_id>/',
        ResultIndependentResearchList.as_view()
    ),
    path('', include(router.urls)),
]
