from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from ford3.models.user import User, ProvinceUser
from ford3.notifier import Notifier
from ford3.enums.open_edu_groups import OpenEduGroups


def send_activation_email(sender, instance, created, **kwargs):
    if created:
        Notifier.send_activation_email(instance)


def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        group_id = [
            group[0] for group in [
                (ob.value, getattr(instance, f'is_{ob.name.lower()}'))
                for ob in OpenEduGroups] if group[1]][0]
        group = Group.objects.get(pk=group_id)
        group.user_set.add(instance)


post_save.connect(send_activation_email, sender=User)
post_save.connect(add_user_to_group, sender=User)
post_save.connect(send_activation_email, sender=ProvinceUser)
post_save.connect(add_user_to_group, sender=ProvinceUser)
