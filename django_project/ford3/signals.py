from django.db.models.signals import post_save
from ford3.models.user import User


def send_activation_email(sender, instance, created, **kwargs):
    if created:
        instance.send_activation_email()


post_save.connect(send_activation_email, sender=User)
