from django.db.models import Count, Q
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from ..models import Doctor
from .serializers import DoctorSerializer


class PageNumberPaginationBy10(PageNumberPagination):
    page_size = 10


@method_decorator(name="list", decorator=swagger_auto_schema(tags=["doctors"]))
@method_decorator(name="retrieve", decorator=swagger_auto_schema(tags=["doctors"]))
class DoctorViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    pagination_class = PageNumberPaginationBy10
    queryset = Doctor.objects.filter(is_active=True)
    serializer_class = DoctorSerializer
    lookup_field = "id"
    permission_classes = [AllowAny]
    search_fields = ["user__first_name", "user__last_name", "user__patronymic", "phone"]
    filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        if self.action == "list":
            if self.request.user.is_authenticated:
                # сортировка чтобы первые были лечащие врачи пациента
                return self.queryset.annotate(
                    treating_doctor=Count(
                        "pacients",
                        distinct=True,
                        filter=Q(pacients__id=self.request.user.pacient.id),
                    ),
                ).order_by(
                    "treating_doctor",
                    "user__first_name",
                    "user__last_name",
                    "user__patronymic",
                )
            return self.queryset
        elif self.action == "retrieve":
            return self.queryset
        else:
            return self.queryset.none()
