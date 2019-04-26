from django.db import models

class Prospect(models.Model):
    name = models.CharField(
        blank=False,
        help_text='Prospect first and last name',
        max_length=150)
    telephone = models.IntegerField(
        blank=False,
        help_text='Prospect telephone number',
        max_length=150)
    email = models.EmailField(
        blank=False,
        help_text='Prospect email address')
