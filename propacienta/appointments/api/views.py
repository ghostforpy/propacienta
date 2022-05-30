from django.db.models import Count, Q
# from drf_yasg import openapi
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
# from rest_framework import status
# from rest_framework.generics import (
#     CreateAPIView,
#     DestroyAPIView,
#     ListAPIView,
#     RetrieveAPIView,
#     get_object_or_404,
# )
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from doctors.utils import request_by_doctor

from .filtersets import DateTimeRangeFilterSet
# from ..models import AppointmentOrder, AppointmentSurvey
# from ..utils import (
#     IsOwnerOfAnalisObject,
#     IsOwnerOfAnalisResultFileAndImageObject,
#     IsOwnerOfAnalisResultObject,
#     RequestByTreatingDoctor,
#     RequestByTreatingDoctorAnalisResult,
#     RequestByTreatingDoctorAnalisResultFileAndImage,
# )
from .serializers import (
    AppointmentOrderDoctorSerializer,
    AppointmentOrderPacientSerializer,
    AppointmentSurveySerializer,
)


class PageNumberPaginationBy10(PageNumberPagination):
    page_size = 10


# @method_decorator(name="update", decorator=swagger_auto_schema(tags=["pacient-appointments"]))
# @method_decorator(name="partial_update", decorator=swagger_auto_schema(tags=["pacient-appointments"]))
@method_decorator(name="list", decorator=swagger_auto_schema(tags=["pacient-appointments"]))
@method_decorator(name="retrieve", decorator=swagger_auto_schema(tags=["pacient-appointments"]))
@method_decorator(name="create", decorator=swagger_auto_schema(tags=["pacient-appointments"]))
@method_decorator(name="destroy", decorator=swagger_auto_schema(tags=["pacient-appointments"]))
class AppointmentOrderPacientViewSet(CreateModelMixin,
                                     RetrieveModelMixin,
                                     DestroyModelMixin,
                                     ListModelMixin,
                                     GenericViewSet):
    serializer_class = AppointmentOrderPacientSerializer
    permission_classes = [IsAuthenticated]
    # pagination_class = PageNumberPaginationBy10

    def get_queryset(self):
        return self.request.user.pacient.appointment_orders.all().select_related(
            "hospital",
            "doctor",
            "doctor__user",
            "doctor_specialization",
            "doctor_sub_specialization"
        )


# @method_decorator(name="update", decorator=swagger_auto_schema(tags=["doctor-appointments"]))
# @method_decorator(name="partial_update", decorator=swagger_auto_schema(tags=["doctor-appointments"]))
@method_decorator(name="list", decorator=swagger_auto_schema(tags=["doctor-appointments"]))
@method_decorator(name="retrieve", decorator=swagger_auto_schema(tags=["doctor-appointments"]))
@method_decorator(name="create", decorator=swagger_auto_schema(tags=["doctor-appointments"]))
@method_decorator(name="destroy", decorator=swagger_auto_schema(tags=["doctor-appointments"]))
class AppointmentOrderDoctorViewSet(CreateModelMixin,
                                    RetrieveModelMixin,
                                    DestroyModelMixin,
                                    ListModelMixin,
                                    GenericViewSet):
    serializer_class = AppointmentOrderDoctorSerializer
    # queryset = AppointmentOrder.objects.all()
    permission_classes = [IsAuthenticated]
    filterset_class = DateTimeRangeFilterSet
    filter_backends = [DjangoFilterBackend]
    # pagination_class = PageNumberPaginationBy10

    def get_queryset(self):
        return self.request.user.doctor.appointment_orders.all().select_related(
            "hospital",
            "pacient",
            "pacient__user",
            "doctor_specialization",
            "doctor_sub_specialization"
        )

    # def paginate_queryset(self, queryset):
    #     if self.request.query_params.get("calendar") == "true":
    #         return None
    #     else:
    #         return super().paginate_queryset(queryset)


# @method_decorator(
#     name="get", decorator=swagger_auto_schema(tags=["auth-requests-private-media"])
# )
# class BaseAuthRetrieveAnalysisResultsView(RetrieveAPIView):
#     permission_classes = [
#         IsOwnerOfAnalisResultFileAndImageObject
#         | RequestByTreatingDoctorAnalisResultFileAndImage
#     ]
#     field_name = None  # str

#     def retrieve(self, request, *args, **kwargs):
#         _ = self.get_object()
#         return Response(status=200)

#     def get_object(self):
#         filename = self.request.headers["Filename"]
#         pacient_id = self.request.headers["Pacientid"]
#         qs = self.queryset.filter(analysis_result__pacient__id=pacient_id).filter(
#             **{self.field_name + "__iendswith": filename}
#         )
#         obj = get_object_or_404(qs)
#         self.check_object_permissions(self.request, obj)
#         return obj


# class AuthRetrieveAnalysisResultsImageView(BaseAuthRetrieveAnalysisResultsView):
#     """
#     View to auth requests AnalysisResultsImage.
#     """

#     serializer_class = AnalysisResultsImageSerializer
#     queryset = AnalysisResultsImage.objects.all()
#     field_name = "image"


# class AuthRetrieveAnalysisResultsFileView(BaseAuthRetrieveAnalysisResultsView):
#     """
#     View to auth requests AnalysisResultsFile.
#     """

#     serializer_class = AnalysisResultsFileSerializer
#     queryset = AnalysisResultsFile.objects.all()
#     field_name = "file"


# @method_decorator(name="post", decorator=swagger_auto_schema(tags=["analysis-results"]))
# @method_decorator(name="get", decorator=swagger_auto_schema(tags=["analysis-results"]))
# class AnalysisResultCreateListView(CreateAPIView, ListAPIView):
#     """
#     View to create and list AnalysisResult.
#     """

#     permission_classes = [
#         IsOwnerOfAnalisResultObject | RequestByTreatingDoctorAnalisResult
#     ]
#     serializer_class = AnalysisResultSerializer
#     queryset = AnalysisResult.objects.all()
#     pagination_class = PageNumberPaginationBy10

#     def list(self, request, *args, **kwargs):
#         """
#         Return a list of all AnalysisResult by pacient id and AnalysisResult id.
#         """
#         pacient_id = kwargs["pacient_id"]
#         analysis_id = kwargs["analysis_id"]
#         self.queryset = AnalysisResult.objects.filter(analysis__id=analysis_id).filter(
#             pacient__id=pacient_id
#         )
#         return super().list(request, *args, **kwargs)


# @method_decorator(
#     name="delete", decorator=swagger_auto_schema(tags=["analysis-results"])
# )
# class AnalysisResultDestoryView(DestroyAPIView):
#     """
#     View to destroy AnalysisResult.
#     """

#     permission_classes = [
#         IsOwnerOfAnalisResultObject | RequestByTreatingDoctorAnalisResult
#     ]
#     serializer_class = AnalysisResultSerializer
#     queryset = AnalysisResult.objects.all()
#     lookup_url_kwarg = "analysis_result_id"


# @method_decorator(
#     name="delete", decorator=swagger_auto_schema(tags=["analysis-results"])
# )
# class AnalysisResultImageDeleteView(DestroyAPIView):
#     queryset = AnalysisResultsImage.objects.all()
#     permission_classes = [IsOwnerOfAnalisObject | RequestByTreatingDoctor]


# @method_decorator(
#     name="delete", decorator=swagger_auto_schema(tags=["analysis-results"])
# )
# class AnalysisResultFileDeleteView(DestroyAPIView):
#     queryset = AnalysisResultsFile.objects.all()
#     permission_classes = [IsOwnerOfAnalisObject | RequestByTreatingDoctor]
