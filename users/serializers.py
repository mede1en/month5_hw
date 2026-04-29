from rest_framework import serializers
from users.models import CustomUser
from django.contrib.auth import authenticate

class RegisterValidateSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'phone_number')

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