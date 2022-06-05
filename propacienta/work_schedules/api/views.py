# from drf_yasg import openapi
from datetime import datetime, timedelta

from django.db.models import Count, F, Min, Prefetch, Q
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
# from rest_framework.generics import (  # CreateAPIView,; DestroyAPIView,; RetrieveAPIView,; get_object_or_404,
#     ListAPIView,
# )
from rest_framework.mixins import (  # , UpdateModelMixin
    ListModelMixin,
    RetrieveModelMixin,
)
# from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ..models import (  # TransferredOperation,; TransferredOperationFile,; TransferredOperationImage,
    NotWorkingPeriod,
    WorkDay,
)
from .filtersets import DateRangeFilterSet
# from ..utils import (
#     IsOwnerOfTransferredOperationImageAndFileObject,
#     IsOwnerOfTransferredOperationImageOrFileObject,
#     IsOwnerOfTransferredOperationObject,
#     RequestByTreatingDoctorTransferredOperation,
#     RequestByTreatingDoctorTransferredOperationImageAndFile,
#     RequestByTreatingDoctorTransferredOperationImageOrFile,
# )
from .serializers import WorkDaySerializer, WorkDayTimeSlotsSerializer

DAYS_FOR_VIEW = 30
# from doctors.utils import request_by_doctor


# class PageNumberPaginationBy10(PageNumberPagination):
#     page_size = 10


class BaseWorkDayViewSet(GenericViewSet):
    queryset = WorkDay.objects.filter(
        date__gte=datetime.now().date(),
        date__lte=(datetime.now() + timedelta(days=DAYS_FOR_VIEW)).date()
        )
    permission_classes = [AllowAny]
    filterset_fields = ["doctor", "hospital", "date"]
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        queryset = self.queryset.prefetch_related(
            Prefetch(
                "doctor__not_working_periods",
                queryset=NotWorkingPeriod.objects.exclude(
                    to__lt=datetime.now().date()
                    ).filter(is_open=True)
            )
        )
        # выполняем cross join всех нерабочих периодов ко всем рабочим дням
        queryset = queryset.annotate(
            since_notwork=F("doctor__not_working_periods__since"),
            to_notwork=F("doctor__not_working_periods__to")
        )
        # убираем дни, которые попали на нерабоиче периоды
        queryset = queryset.exclude(date__range=(F("since_notwork"), F("to_notwork")))
        # убираем повторяющиеся записи сравнением по полю id
        queryset = queryset.distinct("id")
        # print(queryset.query)
        # [print(i.doctor.not_working_periods.all(), i.since_notwork) for i in queryset]
        return queryset


@method_decorator(name="retrieve", decorator=swagger_auto_schema(tags=["workdays"]))
@method_decorator(name="list", decorator=swagger_auto_schema(tags=["workdays"]))
class WorkDaySlotsViewSet(RetrieveModelMixin, ListModelMixin, BaseWorkDayViewSet):
    serializer_class = WorkDayTimeSlotsSerializer
    filterset_class = DateRangeFilterSet

    def get_queryset(self):
        return super().get_queryset().order_by("since").distinct("since")


@method_decorator(name="list", decorator=swagger_auto_schema(tags=["workdays"]))
class WorkDayViewSet(ListModelMixin, BaseWorkDayViewSet):
    serializer_class = WorkDaySerializer

    def get_queryset(self):
        return super().get_queryset().order_by('date').distinct('date')



# @method_decorator(
#     name="get", decorator=swagger_auto_schema(tags=["auth-requests-private-media"])
# )
# class BaseAuthRetrieveTransferredOperationFileAndImageView(RetrieveAPIView):
#     permission_classes = [
#         IsOwnerOfTransferredOperationImageAndFileObject
#         | RequestByTreatingDoctorTransferredOperationImageAndFile
#     ]
#     field_name = None  # str

#     def retrieve(self, request, *args, **kwargs):
#         _ = self.get_object()
#         return Response(status=200)

#     def get_object(self):
#         filename = self.request.headers["Filename"]
#         pacient_id = self.request.headers["Pacientid"]
#         qs = self.queryset.filter(transferred_operation__pacient__id=pacient_id).filter(
#             **{self.field_name + "__iendswith": filename}
#         )
#         obj = get_object_or_404(qs)
#         self.check_object_permissions(self.request, obj)
#         return obj


# class AuthRetrieveTransferredOperationImageView(
#     BaseAuthRetrieveTransferredOperationFileAndImageView
# ):
#     """
#     View to auth requests TransferredOperationImage.
#     """

#     serializer_class = TransferredOperationImageSerializer
#     queryset = TransferredOperationImage.objects.all()
#     field_name = "image"


# class AuthRetrieveTransferredOperationFileView(
#     BaseAuthRetrieveTransferredOperationFileAndImageView
# ):
#     """
#     View to auth requests TransferredOperationFile.
#     """

#     serializer_class = TransferredOperationFileSerializer
#     queryset = TransferredOperationFile.objects.all()
#     field_name = "file"


# @method_decorator(name="post", decorator=swagger_auto_schema(tags=["operations"]))
# @method_decorator(name="get", decorator=swagger_auto_schema(tags=["operations"]))
# class TransferredOperationCreateListView(CreateAPIView, ListAPIView):
#     """
#     View to create and list TransferredOperation.
#     """

#     permission_classes = [
#         IsOwnerOfTransferredOperationObject
#         | RequestByTreatingDoctorTransferredOperation
#     ]
#     serializer_class = TransferredOperationSerializer
#     queryset = TransferredOperation.objects.all()
#     pagination_class = PageNumberPaginationBy10

#     def get_queryset(self):
#         pacient_id = self.kwargs["pacient_id"]
#         qs = super().get_queryset().filter(pacient__id=pacient_id)
#         if "operation" in self.request.GET:
#             qs = qs.filter(operation__id=self.request.GET["operation"])
#         return qs


# @method_decorator(name="delete", decorator=swagger_auto_schema(tags=["operations"]))
# class TransferredOperationDestoryView(DestroyAPIView):
#     """
#     View to destroy TransferredOperation.
#     """

#     permission_classes = [
#         IsOwnerOfTransferredOperationObject
#         | RequestByTreatingDoctorTransferredOperation
#     ]
#     serializer_class = TransferredOperationSerializer
#     queryset = TransferredOperation.objects.all()
#     lookup_url_kwarg = "transferred_operation_id"

#     def get_queryset(self):
#         pacient_id = self.kwargs["pacient_id"]
#         return super().get_queryset().filter(pacient__id=pacient_id)


# @method_decorator(name="delete", decorator=swagger_auto_schema(tags=["operations"]))
# class TransferredOperationFileDeleteView(DestroyAPIView):
#     queryset = TransferredOperationFile.objects.all()
#     permission_classes = [
#         IsOwnerOfTransferredOperationImageOrFileObject
#         | RequestByTreatingDoctorTransferredOperationImageOrFile
#     ]


# @method_decorator(name="delete", decorator=swagger_auto_schema(tags=["operations"]))
# class TransferredOperationImageDeleteView(DestroyAPIView):
#     queryset = TransferredOperationImage.objects.all()
#     permission_classes = [
#         IsOwnerOfTransferredOperationImageOrFileObject
#         | RequestByTreatingDoctorTransferredOperationImageOrFile
#     ]
