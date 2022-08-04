from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.response import Response
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


@method_decorator(name="list", decorator=swagger_auto_schema(tags=["pacients"]))
@method_decorator(name="get_pacients_count", decorator=swagger_auto_schema(tags=["pacients"]))
@method_decorator(name="retrieve", decorator=swagger_auto_schema(tags=["pacients"]))
class PacientViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    pagination_class = PageNumberPaginationBy10
    queryset = Pacient.objects.all()
    serializer_class = PacientSerializer
    lookup_field = "id"
    permission_classes = [RequestByDoctor]
    search_fields = ["user__first_name", "user__last_name", "user__patronymic", "phone"]
    filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        if self.action == "list":
            queryparams = self.request.GET.dict()
            search = queryparams.get("search", None)
            if search is not None and search != "":
                return self.queryset
            doctor = self.request.user.doctor
            return doctor.pacients.all()
        elif self.action == "retrieve":
            return self.queryset
        else:
            return self.queryset.none()

    @action(methods=['get'], detail=False,
            url_path='pacients-count', url_name='pacients-count',
            permission_classes=[AllowAny])
    def get_pacients_count(self, request, *args, **kwargs):
        count = self.queryset.count()
        return Response(data={"pacients_count": count})
