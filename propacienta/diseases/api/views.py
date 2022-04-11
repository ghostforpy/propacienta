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

from ..models import (  # ChronicDisease,
    DischargeEpicris,
    DischargeEpicrisFiles,
    DischargeEpicrisImage,
    Disease,
    TransferredDisease,
)
from ..utils import (
    IsOwnerOfDischargeEpicrisImageAndFileObject,
    IsOwnerOfDischargeEpicrisImageOrFileObject,
    IsOwnerOfTransferredOrChronicDiseaseObject,
    RequestByTreatingDoctorDischargeEpicrisImageAndFile,
    RequestByTreatingDoctorDischargeEpicrisImageOrFile,
    RequestByTreatingDoctorTransferredOrChronicDisease,
)
from .serializers import (  # ChronicDiseaseSerializer,
    DischargeEpicrisFilesSerializer,
    DischargeEpicrisImageSerializer,
    DischargeEpicrisSerializer,
    DiseaseSerializer,
    TransferredDiseaseSerializer,
)


class PageNumberPaginationBy10(PageNumberPagination):
    page_size = 10


@method_decorator(name='list', decorator=swagger_auto_schema(
    tags=["diseases"]
))
class DiseasesViewSet(ListModelMixin, GenericViewSet):
    serializer_class = DiseaseSerializer
    queryset = Disease.objects.all()
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
            disease_type = queryparams.get("diseaseType", None)  # chronic or transferred
            if disease_type in (
                "chronic",
                # "transferred"
            ):
                queryset = self.queryset.annotate(
                    diseases_count=Count(
                        "{}_diseases".format(disease_type),
                        distinct=True,
                        filter=Q(
                            **{"{}_diseases__pacient__id".format(disease_type): pacient_id}
                        )
                    ),
                ).order_by("-diseases_count")
        return queryset


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=["auth-requests-private-media"]
))
class BaseAuthRetrieveDischargeEpicrisFileAndImageView(RetrieveAPIView):
    permission_classes = [IsOwnerOfDischargeEpicrisImageAndFileObject |
                          RequestByTreatingDoctorDischargeEpicrisImageAndFile]
    field_name = None  # str

    def retrieve(self, request, *args, **kwargs):
        _ = self.get_object()
        return Response(status=200)

    def get_object(self):
        filename = self.request.headers['Filename']
        pacient_id = self.request.headers['Pacientid']
        qs = self.queryset.filter(
            discharge_epicris__pacient__id=pacient_id
        ).filter(**{self.field_name+"__iendswith": filename})
        obj = get_object_or_404(qs)
        self.check_object_permissions(self.request, obj)
        return obj


class AuthRetrieveDischargeEpicrisImageView(BaseAuthRetrieveDischargeEpicrisFileAndImageView):
    """
    View to auth requests DischargeEpicrisImage.
    """
    serializer_class = DischargeEpicrisImageSerializer
    queryset = DischargeEpicrisImage.objects.all()
    field_name = "image"


class AuthRetrieveDischargeEpicrisFilesView(BaseAuthRetrieveDischargeEpicrisFileAndImageView):
    """
    View to auth requests DischargeEpicrisFiles.
    """
    serializer_class = DischargeEpicrisFilesSerializer
    queryset = DischargeEpicrisFiles.objects.all()
    field_name = "file"


@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=["transferred-diseases"]
))
@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=["transferred-diseases"]
))
class TransferredDiseaseCreateListView(CreateAPIView, ListAPIView):
    """
    View to create and list TransferredDisease.
    """
    permission_classes = [
        IsOwnerOfTransferredOrChronicDiseaseObject |
        RequestByTreatingDoctorTransferredOrChronicDisease
    ]
    serializer_class = TransferredDiseaseSerializer
    queryset = TransferredDisease.objects.all()
    pagination_class = PageNumberPaginationBy10

    def get_queryset(self):
        pacient_id = self.kwargs["pacient_id"]
        return super().get_queryset().filter(pacient__id=pacient_id)


@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=["transferred-diseases"]
))
class TransferredDiseaseDestoryView(DestroyAPIView):
    """
    View to destroy TransferredDisease.
    """
    permission_classes = [
        IsOwnerOfTransferredOrChronicDiseaseObject |
        RequestByTreatingDoctorTransferredOrChronicDisease
    ]
    serializer_class = TransferredDiseaseSerializer
    queryset = TransferredDisease.objects.all()
    lookup_url_kwarg = 'transferred_disease_id'

    def get_queryset(self):
        pacient_id = self.kwargs["pacient_id"]
        return super().get_queryset().filter(pacient__id=pacient_id)


@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=["analysis-results"]
))
class DischargeEpicrisImageDeleteView(DestroyAPIView):
    queryset = DischargeEpicrisImage.objects.all()
    permission_classes = [
        IsOwnerOfDischargeEpicrisImageOrFileObject |
        RequestByTreatingDoctorDischargeEpicrisImageOrFile
    ]


@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=["analysis-results"]
))
class DischargeEpicrisFileDeleteView(DestroyAPIView):
    queryset = DischargeEpicrisFiles.objects.all()
    permission_classes = [
        IsOwnerOfDischargeEpicrisImageOrFileObject |
        RequestByTreatingDoctorDischargeEpicrisImageOrFile
    ]


# @method_decorator(name='post', decorator=swagger_auto_schema(
#     tags=["chronic-diseases"]
# ))
# @method_decorator(name='get', decorator=swagger_auto_schema(
#     tags=["chronic-diseases"]
# ))
# class ChronicDiseaseCreateListView(CreateAPIView, ListAPIView):
#     """
#     View to create and list ChronicDisease.
#     """
#     permission_classes = [
#         IsOwnerOfTransferredOrChronicDiseaseObject |
#         RequestByTreatingDoctorTransferredOrChronicDisease
#     ]
#     serializer_class = ChronicDiseaseSerializer
#     queryset = ChronicDisease.objects.all()
#     pagination_class = PageNumberPaginationBy10

#     def get_queryset(self):
#         pacient_id = self.kwargs["pacient_id"]
#         return super().get_queryset().filter(pacient__id=pacient_id)


# @method_decorator(name='delete', decorator=swagger_auto_schema(
#     tags=["chronic-diseases"]
# ))
# class ChronicDiseaseDestoryView(DestroyAPIView):
#     """
#     View to destroy ChronicDisease.
#     """
#     permission_classes = [
#         IsOwnerOfTransferredOrChronicDiseaseObject |
#         RequestByTreatingDoctorTransferredOrChronicDisease
#     ]
#     serializer_class = ChronicDiseaseSerializer
#     queryset = ChronicDisease.objects.all()
#     lookup_url_kwarg = 'chronic_disease_id'

#     def get_queryset(self):
#         pacient_id = self.kwargs["pacient_id"]
#         return super().get_queryset().filter(pacient__id=pacient_id)


@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=["chronic-diseases"]
))
@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=["chronic-diseases"]
))
class DischargeEpicrisCreateListView(CreateAPIView, ListAPIView):
    """
    View to create and list DischargeEpicris.
    """
    serializer_class = DischargeEpicrisSerializer
    queryset = DischargeEpicris.objects.all()
    pagination_class = PageNumberPaginationBy10
    permission_classes = [
        IsOwnerOfTransferredOrChronicDiseaseObject |
        RequestByTreatingDoctorTransferredOrChronicDisease
    ]

    def get_queryset(self):
        pacient_id = self.kwargs["pacient_id"]
        disease_id = self.kwargs["disease_id"]
        return super().get_queryset().filter(
            pacient__id=pacient_id,
            chronic_disease__disease__id=disease_id
        )


@method_decorator(name='delete', decorator=swagger_auto_schema(
    tags=["chronic-diseases"]
))
class DischargeEpicrisDestoryView(DestroyAPIView):
    """
    View to destroy DischargeEpicris.
    """
    permission_classes = [
        IsOwnerOfTransferredOrChronicDiseaseObject |
        RequestByTreatingDoctorTransferredOrChronicDisease
    ]
    queryset = DischargeEpicris.objects.all()
    lookup_url_kwarg = 'discharge_epicris_id'

    def get_queryset(self):
        pacient_id = self.kwargs["pacient_id"]
        return super().get_queryset().filter(pacient__id=pacient_id)
