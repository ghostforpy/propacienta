from django.db.models import Count, Q
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters
from rest_framework import status as response_status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ..models import Doctor, DoctorSpecialization
from ..utils import RequestByDoctorOwnerAccount
from .serializers import (
    DoctorSerializer,
    DoctorSpecializationListSerializer,
    DoctorUpdateSerializer,
)


class PageNumberPaginationBy10(PageNumberPagination):
    page_size = 10


@method_decorator(name="delete_avatar", decorator=swagger_auto_schema(tags=["doctors"]))
@method_decorator(name="update", decorator=swagger_auto_schema(tags=["doctors"]))
@method_decorator(
    name="partial_update", decorator=swagger_auto_schema(tags=["doctors"])
)
@method_decorator(
    name="treating_doctor", decorator=swagger_auto_schema(tags=["doctors"])
)
@method_decorator(name="list", decorator=swagger_auto_schema(tags=["doctors"]))
@method_decorator(name="retrieve", decorator=swagger_auto_schema(tags=["doctors"]))
class DoctorViewSet(
    RetrieveModelMixin, UpdateModelMixin, ListModelMixin, GenericViewSet
):
    pagination_class = PageNumberPaginationBy10
    queryset = Doctor.objects.filter(is_active=True).prefetch_related(
        "specializations", "sub_specializations", "hospitals", "user"
    )
    # serializer_class = DoctorSerializer
    lookup_field = "id"
    # permission_classes = [AllowAny]
    search_fields = [
        "user__first_name",
        "user__last_name",
        "user__patronymic",
        # "phone",
        "specializations__title",
        "sub_specializations__title",
    ]
    filter_backends = [filters.SearchFilter]

    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     print(instance, 7777777777777777)
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     print(serializer, 11111111111111)
    #     serializer.is_valid(raise_exception=False)
    #     print(serializer.errors)
    #     print(222222222)
    #     # return
    #     self.perform_update(serializer)

    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         # If 'prefetch_related' has been applied to a queryset, we need to
    #         # forcibly invalidate the prefetch cache on the instance.
    #         instance._prefetched_objects_cache = {}

    #     return Response(serializer.data)

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return DoctorUpdateSerializer
        else:
            return DoctorSerializer

    def get_permissions(self):
        if self.action == "treating_doctor":
            permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update", "delete_avatar"]:
            permission_classes = [RequestByDoctorOwnerAccount]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

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
                    "-treating_doctor",
                    "user__first_name",
                    "user__last_name",
                    "user__patronymic",
                )
            return self.queryset
        elif self.action in [
            "retrieve",
            "treating_doctor",
            "update",
            "partial_update",
            "delete_avatar",
        ]:
            qs = self.queryset
            # if self.request.user.is_authenticated:
            #     qs = self.queryset.prefetch_related("pacients")
            return qs
        else:
            return self.queryset.none()

    @action(
        methods=["post"],
        detail=True,
        url_path="treating_doctor",
        url_name="treating_doctor",
    )
    def treating_doctor(self, request, *args, **kwargs):
        instance = self.get_object()
        pacient = request.user.pacient
        if instance in pacient.treating_doctors.all():
            pacient.treating_doctors.remove(instance)
            status = response_status.HTTP_204_NO_CONTENT
        else:
            pacient.treating_doctors.add(instance)
            status = response_status.HTTP_200_OK
        pacient.save()
        return Response(status=status)

    @action(
        methods=["delete"],
        detail=True,
        url_path="delete_avatar",
        url_name="delete_avatar",
    )
    def delete_avatar(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.avatar.delete()
        status = response_status.HTTP_204_NO_CONTENT
        instance.save()
        return Response(status=status)


@method_decorator(name="list", decorator=swagger_auto_schema(tags=["doctors"]))
class DoctorSpecializationViewSet(ListModelMixin, GenericViewSet):
    queryset = DoctorSpecialization.objects.prefetch_related("sub_specializations")
    serializer_class = DoctorSpecializationListSerializer
    permission_classes = [AllowAny]
