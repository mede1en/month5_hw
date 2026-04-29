from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from users.managers import CustomUserManager
import random

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return self.email



class ConfirmationCode(models.Model):
    code = models.CharField(max_length=7)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def generate_code(self):
        self.code = str(random.randint(10000, 99999))
