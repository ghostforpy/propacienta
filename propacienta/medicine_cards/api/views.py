from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import (IsAuthenticated,
                                        AllowAny,
                                        SAFE_METHODS,
                                        BasePermission)
from .serializers import MedicineCardSerializer
from ..models import MedicineCard
User = get_user_model()

class IsOwnerOfMedicineCardObject(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # # Instance must have an attribute named `owner`.
        print(1111111111,request.user == obj.pacient.user)
        if request.user == obj.pacient.user:
            return True
        return False

#@method_decorator(name='list', decorator=swagger_auto_schema(
#    tags=["users"]
#))

#@method_decorator(name='me', decorator=swagger_auto_schema(
#    tags=["users"]
#))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    tags=["medicine-cards"]
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    tags=["medicine-cards"]
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    tags=["medicine-cards"]
))
class MedicineCardViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = MedicineCardSerializer
    queryset = MedicineCard.objects.all()
    lookup_field = "id"
    permission_classes = [IsOwnerOfMedicineCardObject]

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

#    @action(detail=False)
#    def me(self, request):
#        serializer = MedicineCard(request.user, context={"request": request})
#        return Response(status=status.HTTP_200_OK, data=serializer.data)
