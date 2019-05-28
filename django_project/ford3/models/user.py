from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_province = models.BooleanField(
        'province status', default=False)
    is_provider = models.BooleanField(
        'provider status', default=False)
    is_campus = models.BooleanField(
        'campus status', default=False)
    account_activated = models.BooleanField(default=False)
    provinces = models.ManyToManyField(
        'ford3.Province',
        blank=True)


class ProvinceUser(User):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.is_province = True
        self.username = self.email
        super().save(*args, **kwargs)
    
    @property
    def providers(self):
        Provider.objects.all.filter(province_id=self.province_id)
