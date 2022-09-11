from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ..coturn import get_coturn_credentials


@method_decorator(name="get_credentials", decorator=swagger_auto_schema(tags=["coturn"]))
class CoturnViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]

    @action(methods=['get'], detail=False,
            url_path='get-credentials', url_name='get-credentials')
    def get_credentials(self, request, *args, **kwargs):
        user_id = request.user.id
        credentials = get_coturn_credentials(user_id=user_id)
        return Response(data=credentials)
