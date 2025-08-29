from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone_number = models.CharField("Téléphone", max_length=20, blank=True, null=True)
    country = models.CharField("Pays", max_length=60, blank=True, null=True)

    def __str__(self):
        return self.username
