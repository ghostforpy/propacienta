# from drf_yasg import openapi
from django.db.models import Count, Q
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    get_object_or_404,
)
from rest_framework.mixins import ListModelMixin  # RetrieveModelMixin, UpdateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from doctors.utils import request_by_doctor

from ..models import (
    Operation,
    TransferredOperation,
    TransferredOperationFile,
    TransferredOperationImage,
)
from ..utils import (
    IsOwnerOfTransferredOperationImageAndFileObject,
    IsOwnerOfTransferredOperationImageOrFileObject,
    IsOwnerOfTransferredOperationObject,
    RequestByTreatingDoctorTransferredOperation,
    RequestByTreatingDoctorTransferredOperationImageAndFile,
    RequestByTreatingDoctorTransferredOperationImageOrFile,
)
from .serializers import (
    OperationSerializer,
    TransferredOperationFileSerializer,
    TransferredOperationImageSerializer,
    TransferredOperationSerializer,
)


class PageNumberPaginationBy10(PageNumberPagination):
    page_size = 10


@method_decorator(name="list", decorator=swagger_auto_schema(tags=["operations"]))
class OperationViewSet(ListModelMixin, GenericViewSet):
    serializer_class = OperationSerializer
    queryset = Operation.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        doctor = request_by_doctor(self.request)
        queryparams = self.request.GET.dict()
        queryset = self.queryset
        if doctor is not None:
            pacient_id = queryparams.get("pacientId", None)
            pacient = doctor.pacients.filter(id=pacient_id).count()
            if pacient == 0:  # проверить
                pacient_id = 0
        else:
            pacient_id = self.request.user.pacient.id
        if pacient_id != 0:
            queryset = self.queryset.annotate(
                operation_count=Count(
                    "transferred_operations",
                    distinct=True,
                    filter=Q(**{"transferred_operations__pacient__id": pacient_id}),
                ),
            ).order_by("-operation_count")
        return queryset


@method_decorator(
    name="get", decorator=swagger_auto_schema(tags=["auth-requests-private-media"])
)
class BaseAuthRetrieveTransferredOperationFileAndImageView(RetrieveAPIView):
    permission_classes = [
        IsOwnerOfTransferredOperationImageAndFileObject
        | RequestByTreatingDoctorTransferredOperationImageAndFile
    ]
    field_name = None  # str

    def retrieve(self, request, *args, **kwargs):
        _ = self.get_object()
        return Response(status=200)

    def get_object(self):
        filename = self.request.headers["Filename"]
        pacient_id = self.request.headers["Pacientid"]
        qs = self.queryset.filter(transferred_operation__pacient__id=pacient_id).filter(
            **{self.field_name + "__iendswith": filename}
        )
        obj = get_object_or_404(qs)
        self.check_object_permissions(self.request, obj)
        return obj


class AuthRetrieveTransferredOperationImageView(
    BaseAuthRetrieveTransferredOperationFileAndImageView
):
    """
    View to auth requests TransferredOperationImage.
    """

    serializer_class = TransferredOperationImageSerializer
    queryset = TransferredOperationImage.objects.all()
    field_name = "image"


class AuthRetrieveTransferredOperationFileView(
    BaseAuthRetrieveTransferredOperationFileAndImageView
):
    """
    View to auth requests TransferredOperationFile.
    """

    serializer_class = TransferredOperationFileSerializer
    queryset = TransferredOperationFile.objects.all()
    field_name = "file"


@method_decorator(name="post", decorator=swagger_auto_schema(tags=["operations"]))
@method_decorator(name="get", decorator=swagger_auto_schema(tags=["operations"]))
class TransferredOperationCreateListView(CreateAPIView, ListAPIView):
    """
    View to create and list TransferredOperation.
    """

    permission_classes = [
        IsOwnerOfTransferredOperationObject
        | RequestByTreatingDoctorTransferredOperation
    ]
    serializer_class = TransferredOperationSerializer
    queryset = TransferredOperation.objects.all()
    pagination_class = PageNumberPaginationBy10

    def get_queryset(self):
        pacient_id = self.kwargs["pacient_id"]
        qs = super().get_queryset().filter(pacient__id=pacient_id)
        if "operation" in self.request.GET:
            qs = qs.filter(operation__id=self.request.GET["operation"])
        return qs


@method_decorator(name="delete", decorator=swagger_auto_schema(tags=["operations"]))
class TransferredOperationDestoryView(DestroyAPIView):
    """
    View to destroy TransferredOperation.
    """

    permission_classes = [
        IsOwnerOfTransferredOperationObject
        | RequestByTreatingDoctorTransferredOperation
    ]
    serializer_class = TransferredOperationSerializer
    queryset = TransferredOperation.objects.all()
    lookup_url_kwarg = "transferred_operation_id"

    def get_queryset(self):
        pacient_id = self.kwargs["pacient_id"]
        return super().get_queryset().filter(pacient__id=pacient_id)


@method_decorator(name="delete", decorator=swagger_auto_schema(tags=["operations"]))
class TransferredOperationFileDeleteView(DestroyAPIView):
    queryset = TransferredOperationFile.objects.all()
    permission_classes = [
        IsOwnerOfTransferredOperationImageOrFileObject
        | RequestByTreatingDoctorTransferredOperationImageOrFile
    ]


@method_decorator(name="delete", decorator=swagger_auto_schema(tags=["operations"]))
class TransferredOperationImageDeleteView(DestroyAPIView):
    queryset = TransferredOperationImage.objects.all()
    permission_classes = [
        IsOwnerOfTransferredOperationImageOrFileObject
        | RequestByTreatingDoctorTransferredOperationImageOrFile
    ]
