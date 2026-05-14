import os
import requests
from django.utils import timezone
from django.db import transaction
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from users.serializers import OAuthCodeSerializer

User = get_user_model()


class GoogleLoginAPIView(CreateAPIView):
    serializer_class = OAuthCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data["code"]

        token_response = requests.post(
            url="https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
                "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
                "redirect_uri": os.environ.get("GOOGLE_REDIRECT_URI"),
                "grant_type": "authorization_code"
            }
        )

        if token_response.status_code != 200:
            return Response(
                {"error": f"Failed to get access token: {token_response.text}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        token_data = token_response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            return Response(
                {"error": f"Invalid access token: {token_data}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_info_response = requests.get(
            url="https://www.googleapis.com/oauth2/v3/userinfo",
            params={"alt": "json"},
            headers={"Authorization": f"Bearer {access_token}"}
        )

        if user_info_response.status_code != 200:
            return Response(
                {"error": "Failed to get user info from Google"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_info = user_info_response.json()
        print(f"USER_INFO: {user_info}")

        email = user_info.get("email")
        if not email:
            return Response(
                {"error": "Email not provided by Google"},
                status=status.HTTP_400_BAD_REQUEST
            )

        first_name = user_info.get("given_name", "")
        last_name = user_info.get("family_name", "")

        with transaction.atomic():
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'registration_source': 'google',
                    'is_active': True,
                    'last_login_date': timezone.now(),
                }
            )

            if not created:
                if not user.first_name and first_name:
                    user.first_name = first_name
                if not user.last_name and last_name:
                    user.last_name = last_name

                user.last_login_date = timezone.now()

                if not user.is_active:
                    user.is_active = True

                if not user.registration_source:
                    user.registration_source = 'google'

                user.save()

        refresh = RefreshToken.for_user(user)
        refresh["email"] = user.email
        refresh["first_name"] = user.first_name
        refresh["last_name"] = user.last_name

        return Response(
            {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "is_active": user.is_active,
                    "last_login_date": user.last_login_date,
                    "registration_source": user.registration_source,
                }
            },
            status=status.HTTP_200_OK
        )