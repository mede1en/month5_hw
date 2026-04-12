from django.contrib.auth.models import User
from django.db import models
import random

class ConfirmationCode(models.Model):
    code = models.CharField(max_length=7)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def generate_code(self):
        self.code = random.randint(10000, 99999)
