from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from ford3.models.user import User, ProvinceUser
from ford3.notifier import Notifier
from ford3.models.qualification import Qualification
from ford3.models.campus import Campus
from ford3.completion_audit.completion_audit import CompletionAudit, CAMPUS_COMPLETION_RULES, QUALIFICATION_COMPLETION_RULES  # noqa


def send_activation_email(sender, instance, created, **kwargs):
    if created:
        Notifier.send_activation_email(instance)


def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser or instance.is_staff:
            return
        group = Group.objects.get(
                pk=instance.edu_group.value)
        group.user_set.add(instance)


def audit_for_publish(sender, instance, created, **kwargs):
    instance.audit_for_publish()


def campus_completion_audit(sender, instance, created, **kwargs):

    completion_rate = CompletionAudit(
        instance, CAMPUS_COMPLETION_RULES).run()
    instance.completion_rate = completion_rate
    instance.save()


post_save.connect(send_activation_email, sender=User)
post_save.connect(add_user_to_group, sender=User)
post_save.connect(send_activation_email, sender=ProvinceUser)
post_save.connect(add_user_to_group, sender=ProvinceUser)
post_save.connect(audit_for_publish, sender=Qualification)
post_save.connect(campus_completion_audit, sender=Campus)
