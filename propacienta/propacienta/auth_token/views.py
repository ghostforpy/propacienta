from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import login
#from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import EmailAuthTokenSerializer
from django.views.decorators.csrf import csrf_exempt

class EmailObtainAuthToken(ObtainAuthToken):
    serializer_class = EmailAuthTokenSerializer

    #@csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        #token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        return Response({'is_auth': True})

obtain_auth_token = EmailObtainAuthToken.as_view()