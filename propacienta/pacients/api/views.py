from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission
from rest_framework.viewsets import GenericViewSet

from doctors.utils import request_by_doctor

from ..models import Pacient
from .serializers import PacientSerializer


class RequestByDoctor(BasePermission):
    """
    Object-level permission to only allow requests by active doctors.
    """
    def has_permission(self, request, view):
        return request_by_doctor(request) is not None

    def has_object_permission(self, request, view, obj):
        doctor = request_by_doctor(request)
        if doctor is not None:
            return doctor in obj.treating_doctors.all()
        return False


class PageNumberPaginationBy10(PageNumberPagination):
    page_size = 10


@method_decorator(name='list', decorator=swagger_auto_schema(
   tags=["pacients"]
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
   tags=["pacients"]
))
class PacientViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    pagination_class = PageNumberPaginationBy10
    queryset = Pacient.objects.all()
    serializer_class = PacientSerializer
    lookup_field = "id"
    permission_classes = [RequestByDoctor]

    # def get_permissions(self):

    #     if self.action == 'list':
    #         permission_classes = [AllowAny]
    #     elif self.action in ['my_list', 'create', 'create_by_breport']:
    #         permission_classes = [IsAuthenticated]
    #     elif self.action in [
    #         'get_updated_portfolio',
    #         'update',
    #         'partial_update',
    #         'private'
    #     ]:
    #         permission_classes = [IsOwnerOfPortfolioObject]
    #         #permission_classes = [IsOwnerOrReadOnlyAuthorized]
    #     elif self.action in ['follow', 'like']:
    #         permission_classes = [FollowLikePermission]
    #     else:
    #        # permission_classes = [IsOwnerOrReadOnlyAuthorized]
    #         permission_classes = [IsAuthenticated]
    #     return [permission() for permission in permission_classes]
