from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import UserSerializerz

User = get_user_model()

@method_decorator(name='list', decorator=swagger_auto_schema(
    tags=["users"]
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    tags=["users"]
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    tags=["users"]
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    tags=["users"]
))
@method_decorator(name='me', decorator=swagger_auto_schema(
    tags=["users"]
))
class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializerz
    queryset = User.objects.all()
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializerz(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
