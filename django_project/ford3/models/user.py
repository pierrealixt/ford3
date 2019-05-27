from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_province = models.BooleanField(
        'province status', default=False)
    is_provider = models.BooleanField(
        'provider status', default=False)
    is_campus = models.BooleanField(
        'campus status', default=False)
