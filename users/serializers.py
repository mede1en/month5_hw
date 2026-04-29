from rest_framework import serializers
from users.models import CustomUser
from django.contrib.auth import authenticate

class RegisterValidateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(required=False)

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class LoginValidateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'],
                            password=data['password'])
        if not user:
            raise serializers.ValidationError("Incorrect email or password.")
        return user