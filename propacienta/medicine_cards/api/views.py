from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, DestroyAPIView, CreateAPIView
from rest_framework.mixins import (ListModelMixin, RetrieveModelMixin,
                                    UpdateModelMixin)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import (IsAuthenticated,
                                        AllowAny,
                                        SAFE_METHODS,
                                        BasePermission)
from rest_framework.pagination import PageNumberPagination
from doctors.utils import request_by_doctor, RequestByDoctor
from .serializers import (MedicineCardSerializer,
                            IndependentResearchSerializer,
                            ResultIndependentResearchSerializer)
from ..models import MedicineCard, IndependentResearch, ResultIndependentResearch
User = get_user_model()


class PageNumberPaginationBy50(PageNumberPagination):
    page_size = 50

class IsOwnerOfMedicineCardObject(BasePermission):
    """
    Object-level permission to only allow owners of an object.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # # Instance must have an attribute named `owner`.
        if request.user == obj.pacient.user:
            return True
        return False


class IsOwnerOfResultIndependentResearchObjects(BasePermission):
    """
    Object-level permission to only allow owners of an object.
    """
    def has_permission(self, request, view):
        #print('has perm', view, view.args, view.kwargs)
        return request.user.pacient.id == view.kwargs.get('pacient_id')
        #return request_by_doctor(request) is not None

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # # Instance must have an attribute named `owner`.
        if request.user == obj.medicine_card.pacient.user:
            return True
        return False


@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    tags=["medicine-cards"]
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    tags=["medicine-cards"]
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    tags=["medicine-cards"]
))
class MedicineCardViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = MedicineCardSerializer
    queryset = MedicineCard.objects.all()
    lookup_field = "id"
    permission_classes = [IsOwnerOfMedicineCardObject|RequestByDoctor]

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)


@method_decorator(name='list', decorator=swagger_auto_schema(
    tags=["independent-research"]
))
class IndependentResearchViewSet(ListModelMixin, GenericViewSet):
    serializer_class = IndependentResearchSerializer
    queryset = IndependentResearch.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated]

@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=["independent-research-results"]
))
@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=["independent-research-results"]
))
class ResultIndependentResearchCreateList(CreateAPIView, ListAPIView):
    """
    View to create and list ResultIndependentResearch.
    """
    permission_classes = [IsOwnerOfResultIndependentResearchObjects|RequestByDoctor]
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


@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=["independent-research-results"]
))
class ResultIndependentResearchDestory(DestroyAPIView):
    """
    View to destroy ResultIndependentResearch.
    """
    permission_classes = [IsOwnerOfResultIndependentResearchObjects|RequestByDoctor]
    serializer_class = ResultIndependentResearchSerializer
    queryset = ResultIndependentResearch.objects.all()
    lookup_url_kwarg = 'independent_research_result_id'

