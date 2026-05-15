from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)


    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    last_login_date = models.DateTimeField(blank=True, null=True)
    registration_source = models.CharField(
        max_length=20,
        choices=[
            ('local', 'Local'),
            ('google', 'Google'),
            ('facebook', 'Facebook'),
        ],
        default='local',
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    birthdate = models.DateField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [] 

    def __str__(self):
        return self.email or ''

