from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self,email, password = None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(' is_staff must be True.')
        if extra_fields.get('is_supersuer') is not True:
            raise ValueError(' is_superuser must be True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError(' is_active must be True.')
        if not extra_fields.get('phone_number'):
            raise ValueError('phone_number must be True')
        return self.create_user(email, password=None, **extra_fields)
