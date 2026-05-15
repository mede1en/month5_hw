from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone
from . import utils
CustomUser = get_user_model()


class OAuthCodeSerializer(serializers.Serializer):
    code = serializers.CharField()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["is_staff"] = user.is_staff
        token["first_name"] = user.first_name or ''
        token["last_name"] = user.last_name or ''
        return token


class UserBaseSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=150)
    password = serializers.CharField()


class AuthValidateSerializer(UserBaseSerializer):
    pass


class RegisterValidateSerializer(UserBaseSerializer):
    phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    birthdate = serializers.DateField(required=False, allow_null=True)

    def validate_email(self, email):
        try:
            CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return email
        raise ValidationError("Пользователь уже существует!")


class ConfirmationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get("code")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Пользователь не существует!")

        if not utils.verify_confirmation_code(email, code):
            raise serializers.ValidationError("неверный код подтверждения")

        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data['user']
        user.is_active = True
        user.save()



class GoogleUserInfoSerializer(serializers.Serializer):
    email = serializers.EmailField()
    given_name = serializers.CharField(required=False, allow_blank=True)
    family_name = serializers.CharField(required=False, allow_blank=True)