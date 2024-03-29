from django.db.models import Count, Q

# from drf_yasg import openapi
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    get_object_or_404,
)
from rest_framework.mixins import ListModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from doctors.utils import request_by_doctor

from ..models import Analysis, AnalysisResult, AnalysisResultsFile, AnalysisResultsImage
from ..utils import (
    IsOwnerOfAnalisObject,
    IsOwnerOfAnalisResultFileAndImageObject,
    IsOwnerOfAnalisResultObject,
    RequestByTreatingDoctor,
    RequestByTreatingDoctorAnalisResult,
    RequestByTreatingDoctorAnalisResultFileAndImage,
)
from .serializers import (
    AnalysisResultSerializer,
    AnalysisResultsFileSerializer,
    AnalysisResultsImageSerializer,
    AnalysisSimpleSerializer,
)


class PageNumberPaginationBy10(PageNumberPagination):
    page_size = 10


@method_decorator(name="list", decorator=swagger_auto_schema(tags=["analisys"]))
class AnalysisViewSet(ListModelMixin, GenericViewSet):
    serializer_class = AnalysisSimpleSerializer
    queryset = Analysis.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        doctor = request_by_doctor(self.request)
        if doctor is not None:
            queryparams = self.request.GET.dict()
            pacient_id = queryparams.get("pacientId", None)
            pacient = doctor.pacients.filter(id=pacient_id).count()
            if pacient == 0:  # проверить
                pacient_id = 0
                # queryset = self.queryset.annotate(
                #         results_count=Count(
                #             "analysi_results",
                #             distinct=False,
                #             filter=Q(analysi_results__pacient__id=pacient_id)
                #         ),
                #     )
        else:
            pacient_id = self.request.user.pacient.id
        if pacient_id != 0:
            queryset = self.queryset.annotate(
                results_count=Count(
                    "analysi_results",
                    distinct=False,
                    filter=Q(analysi_results__pacient__id=pacient_id),
                ),
            ).order_by("-results_count")
        else:
            queryset = self.queryset
        return queryset


@method_decorator(
    name="get", decorator=swagger_auto_schema(tags=["auth-requests-private-media"])
)
class BaseAuthRetrieveAnalysisResultsView(RetrieveAPIView):
    permission_classes = [
        IsOwnerOfAnalisResultFileAndImageObject
        | RequestByTreatingDoctorAnalisResultFileAndImage
    ]
    field_name = None  # str

    def retrieve(self, request, *args, **kwargs):
        _ = self.get_object()
        return Response(status=200)

    def get_object(self):
        filename = self.request.headers["Filename"]
        pacient_id = self.request.headers["Pacientid"]
        qs = self.queryset.filter(analysis_result__pacient__id=pacient_id).filter(
            **{self.field_name + "__iendswith": filename}
        )
        obj = get_object_or_404(qs)
        self.check_object_permissions(self.request, obj)
        return obj


class AuthRetrieveAnalysisResultsImageView(BaseAuthRetrieveAnalysisResultsView):
    """
    View to auth requests AnalysisResultsImage.
    """

    serializer_class = AnalysisResultsImageSerializer
    queryset = AnalysisResultsImage.objects.all()
    field_name = "image"


class AuthRetrieveAnalysisResultsFileView(BaseAuthRetrieveAnalysisResultsView):
    """
    View to auth requests AnalysisResultsFile.
    """

    serializer_class = AnalysisResultsFileSerializer
    queryset = AnalysisResultsFile.objects.all()
    field_name = "file"


@method_decorator(name="post", decorator=swagger_auto_schema(tags=["analysis-results"]))
@method_decorator(name="get", decorator=swagger_auto_schema(tags=["analysis-results"]))
class AnalysisResultCreateListView(CreateAPIView, ListAPIView):
    """
    View to create and list AnalysisResult.
    """

    permission_classes = [
        IsOwnerOfAnalisResultObject | RequestByTreatingDoctorAnalisResult
    ]
    serializer_class = AnalysisResultSerializer
    queryset = AnalysisResult.objects.all()
    pagination_class = PageNumberPaginationBy10

    def list(self, request, *args, **kwargs):
        """
        Return a list of all AnalysisResult by pacient id and AnalysisResult id.
        """
        pacient_id = kwargs["pacient_id"]
        analysis_id = kwargs["analysis_id"]
        self.queryset = AnalysisResult.objects.filter(analysis__id=analysis_id).filter(
            pacient__id=pacient_id
        )
        return super().list(request, *args, **kwargs)


@method_decorator(
    name="delete", decorator=swagger_auto_schema(tags=["analysis-results"])
)
class AnalysisResultDestoryView(DestroyAPIView):
    """
    View to destroy AnalysisResult.
    """

    permission_classes = [
        IsOwnerOfAnalisResultObject | RequestByTreatingDoctorAnalisResult
    ]
    serializer_class = AnalysisResultSerializer
    queryset = AnalysisResult.objects.all()
    lookup_url_kwarg = "analysis_result_id"


@method_decorator(
    name="delete", decorator=swagger_auto_schema(tags=["analysis-results"])
)
class AnalysisResultImageDeleteView(DestroyAPIView):
    queryset = AnalysisResultsImage.objects.all()
    permission_classes = [IsOwnerOfAnalisObject | RequestByTreatingDoctor]


@method_decorator(
    name="delete", decorator=swagger_auto_schema(tags=["analysis-results"])
)
class AnalysisResultFileDeleteView(DestroyAPIView):
    queryset = AnalysisResultsFile.objects.all()
    permission_classes = [IsOwnerOfAnalisObject | RequestByTreatingDoctor]
