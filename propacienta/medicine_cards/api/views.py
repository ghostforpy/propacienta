from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema

# from rest_framework import status
# from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (  # SAFE_METHODS,; AllowAny,; BasePermission,
    IsAuthenticated,
)

# from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ..models import IndependentResearch, MedicineCard, ResultIndependentResearch
from ..utils import (
    IsOwnerOfMedicineCardObject,
    IsOwnerOfResultIndependentResearchObjects,
    RequestByTreatingDoctorMedicineCard,
    RequestByTreatingDoctorResultIndependentResearch,
)
from .serializers import (
    IndependentResearchSerializer,
    MedicineCardSerializer,
    ResultIndependentResearchSerializer,
)

User = get_user_model()


class PageNumberPaginationBy50(PageNumberPagination):
    page_size = 50


@method_decorator(
    name="retrieve", decorator=swagger_auto_schema(tags=["medicine-cards"])
)
@method_decorator(name="update", decorator=swagger_auto_schema(tags=["medicine-cards"]))
@method_decorator(
    name="partial_update", decorator=swagger_auto_schema(tags=["medicine-cards"])
)
class MedicineCardViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = MedicineCardSerializer
    queryset = MedicineCard.objects.all()
    lookup_field = "id"
    permission_classes = [
        IsOwnerOfMedicineCardObject | RequestByTreatingDoctorMedicineCard
    ]

    # def get_queryset(self, *args, **kwargs):
    #     if req
    #     assert isinstance(self.request.user.id, int)
    #     return self.queryset.filter(id=self.request.user.id)


@method_decorator(
    name="list", decorator=swagger_auto_schema(tags=["independent-research"])
)
class IndependentResearchViewSet(ListModelMixin, GenericViewSet):
    serializer_class = IndependentResearchSerializer
    queryset = IndependentResearch.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated]


@method_decorator(
    name="post", decorator=swagger_auto_schema(tags=["independent-research-results"])
)
@method_decorator(
    name="get", decorator=swagger_auto_schema(tags=["independent-research-results"])
)
class ResultIndependentResearchCreateList(CreateAPIView, ListAPIView):
    """
    View to create and list ResultIndependentResearch.
    """

    permission_classes = [
        IsOwnerOfResultIndependentResearchObjects
        | RequestByTreatingDoctorResultIndependentResearch
    ]
    serializer_class = ResultIndependentResearchSerializer
    queryset = ResultIndependentResearch.objects.all()
    pagination_class = PageNumberPaginationBy50

    def list(self, request, *args, **kwargs):
        """
        Return a list of all ResultIndependentResearch by pacient id and IndependentResearch id.
        """
        pacient_id = kwargs["pacient_id"]
        independent_research_id = kwargs["independent_research_id"]
        self.queryset = ResultIndependentResearch.objects.filter(
            independent_research__id=independent_research_id
        ).filter(medicine_card__pacient__id=pacient_id)
        return super().list(request, *args, **kwargs)


@method_decorator(
    name="delete", decorator=swagger_auto_schema(tags=["independent-research-results"])
)
class ResultIndependentResearchDestory(DestroyAPIView):
    """
    View to destroy ResultIndependentResearch.
    """

    permission_classes = [
        IsOwnerOfResultIndependentResearchObjects
        | RequestByTreatingDoctorResultIndependentResearch
    ]
    serializer_class = ResultIndependentResearchSerializer
    queryset = ResultIndependentResearch.objects.all()
    lookup_url_kwarg = "independent_research_result_id"
