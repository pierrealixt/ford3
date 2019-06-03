from django.core.validators import RegexValidator
from django.db import models


class Prospect(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{10,15}$',
        message=
        "Phone number must be at least 10 digits and at max 15 digits."
        "It can start with +(country code)")

    name = models.CharField(
        help_text='Prospect first and last name',
        max_length=150,
        verbose_name='Name (required)')
    telephone = models.CharField(
        blank=True,
        help_text='Prospect telephone number',
        validators=[phone_regex],
        max_length=16)
    email = models.EmailField(
        help_text='Prospect email address',
        verbose_name='Email (required)')

    def __str__(self):
        return self.name
