from django.db.models import Count, F, Max, Q
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
from rest_framework.mixins import (  # CreateModelMixin,; RetrieveModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ..models import DialogMessage
# from .filtersets import DialogMessageFilterSet
# from ..models import AppointmentOrder, AppointmentSurvey
# from ..utils import (
#     IsOwnerOfAnalisObject,
#     IsOwnerOfAnalisResultFileAndImageObject,
#     IsOwnerOfAnalisResultObject,
#     RequestByTreatingDoctor,
#     RequestByTreatingDoctorAnalisResult,
#     RequestByTreatingDoctorAnalisResultFileAndImage,
# )
from .serializers import DialogMessageSerializer, DialogSerializer


class PageNumberPaginationBy30(PageNumberPagination):
    page_size = 10


# @method_decorator(name="retrieve", decorator=swagger_auto_schema(tags=["pacient-appointments"]))
# @method_decorator(name="create", decorator=swagger_auto_schema(tags=["pacient-appointments"]))
# @method_decorator(name="destroy", decorator=swagger_auto_schema(tags=["pacient-appointments"]))
@method_decorator(name="list", decorator=swagger_auto_schema(tags=["chats"]))
class DialogViewSet(ListModelMixin,
                    GenericViewSet):
    serializer_class = DialogSerializer
    permission_classes = [IsAuthenticated]
    # pagination_class = PageNumberPaginationBy10

    def get_queryset(self):
        return self.request.user.dialogs.all().prefetch_related(
            "members",
            "members__pacient",
            "members__doctor",
            "members__pacient__medicine_card",
            "messages"
        ).annotate(
            Max("messages__created_at")
            # добавляет аннотацию с датой самого последнего сообщения
        ).annotate(
            messages__count=Count(
                # добавляет аннотацию с количеством непрочитанных сообщений
                "messages",
                filter=Q(messages__read_by_the_user=False) & ~Q(messages__sender=self.request.user)
                # фильтр для непрочитанных сообщений, где пользователь не является отправителем
            )
        ).annotate(
            last=Max(
                # добавляет аннотацию с датами последних непрочитанных сообщений
                "messages__created_at",
                filter=Q(messages__read_by_the_user=False) & ~Q(messages__sender=self.request.user)
                # фильтр для непрочитанных сообщений, где пользователь не является отправителем
            )
        ).order_by(F("last").desc(nulls_last=True), "-messages__created_at__max")
        # сортировка по непрочитанным сообщениям, потом по последним сообщениям

# @method_decorator(name="update", decorator=swagger_auto_schema(tags=["doctor-appointments"]))
# @method_decorator(name="partial_update", decorator=swagger_auto_schema(tags=["doctor-appointments"]))
@method_decorator(name="list", decorator=swagger_auto_schema(tags=["chats"]))
@method_decorator(name="destroy", decorator=swagger_auto_schema(tags=["chats"]))
class DialogMessageViewSet(DestroyModelMixin,
                           ListModelMixin,
                           GenericViewSet):
    serializer_class = DialogMessageSerializer
    permission_classes = [IsAuthenticated]
    # filterset_class = DialogMessageFilterSet
    filterset_fields = ['dialog']
    filter_backends = [DjangoFilterBackend]
    pagination_class = PageNumberPaginationBy30

    def get_queryset(self):
        if self.action == 'destroy':
            return self.request.user.dialog_messages.all()
        return DialogMessage.objects.filter(
            dialog__in=self.request.user.dialogs.all()
        ).order_by("-created_at")
