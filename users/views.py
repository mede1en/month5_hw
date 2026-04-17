from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import  status
from .serializers import RegisterValidateSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import ConfirmationCode
from rest_framework.views import APIView

class AuthAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)
            return Response(data={'key': token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED)

#hw5
class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.create_user(username=username,
                                        password=password)
        user.is_active=False
        user.save()

        code = ConfirmationCode.objects.create(user=user)
        code.generate_code()
        code.save()

        return Response(status=status.HTTP_201_CREATED,
                        data={'user_id': user.id,
                              'code': code.code})

class ConfirmAPIView(APIView):
    def post(self, request):
        code = request.data.get('code')
        try:
            confirmation = ConfirmationCode.objects.get(code=code)
        except ConfirmationCode.DoesNotExist:
            return Response({'error': 'Invalid code'},
                            status=status.HTTP_404_NOT_FOUND)
        return Response('Congratulations!')

        user = confirmation.user
        user.is_active=True
        user.save()

        return Response(status=status.HTTP_201_CREATED,)