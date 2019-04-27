from django.db import models


class Prospect(models.Model):
    name = models.CharField(
        help_text='Prospect first and last name',
        max_length=150,
        verbose_name='Name (required)')
    telephone = models.CharField(
        blank=True,
        help_text='Prospect telephone number',
        max_length=150)
    email = models.EmailField(
        help_text='Prospect email address',
        verbose_name='Email (required)')

    def __str__(self):
        return self.name
