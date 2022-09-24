from django.db.models import F, Q
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ..coturn import get_coturn_credentials
from ..models import WebDial
from .filtersets import DateTimeRangeFilterSet
from .serializers import DialSerializer


class PageNumberPaginationBy50(PageNumberPagination):
    page_size = 50


@method_decorator(name="get_credentials", decorator=swagger_auto_schema(tags=["coturn"]))
class CoturnViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]

    @action(methods=['get'], detail=False,
            url_path='get-credentials', url_name='get-credentials')
    def get_credentials(self, request, *args, **kwargs):
        user_id = request.user.id
        credentials = get_coturn_credentials(user_id=user_id)
        return Response(data=credentials)


@method_decorator(name="list", decorator=swagger_auto_schema(tags=["webdials"]))
class DialsViewSet(ListModelMixin, GenericViewSet):
    serializer_class = DialSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = DateTimeRangeFilterSet
    queryset = WebDial.objects.all()
    pagination_class = PageNumberPaginationBy50
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return super().get_queryset().filter(
            # отображаем вызовы, в которых пользователь является
            # инициатором или вызываемым
            Q(initiator=self.request.user) | Q(opponent=self.request.user)
        ).exclude(
            # не отображать вызовы, которые не состоялись и в которых
            # пользователь был вызываемым
            Q(webdial_happen=False) & Q(opponent=self.request.user)
        ).order_by('-start_webdial')
