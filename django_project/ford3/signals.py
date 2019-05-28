from django.db.models.signals import post_save
from ford3.models.user import User, ProvinceUser
from ford3.notifier import Notifier


def send_activation_email(sender, instance, created, **kwargs):
    if created:
        Notifier.send_activation_email(instance)


post_save.connect(send_activation_email, sender=User)
post_save.connect(send_activation_email, sender=ProvinceUser)
