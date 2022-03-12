from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.urls import path, include
from .views import MedicineCardViewSet


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


router.register('medicine-cards', MedicineCardViewSet, basename='medicine-cards')
app_name = "medicine-cards"

urlpatterns = [
    path('', include(router.urls)),
]
