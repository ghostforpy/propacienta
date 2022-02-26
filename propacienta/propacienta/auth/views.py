from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import login, logout
#from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import EmailAuthTokenSerializer
#from django.views.decorators.csrf import csrf_exempt

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

login_view = EmailObtainAuthToken.as_view()


class LogoutView(APIView):
    def post(self,request):
        logout(request)
        return Response({'is_auth': False})

logout_view = LogoutView.as_view()