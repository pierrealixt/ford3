from django.core.management import call_command
from django.core.management.base import BaseCommand
from ford3.models.user import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Create a superuser and activate it.
        """
        call_command('createsuperuser')
        user = User.objects.last()
        user.is_active = True
        user.save()
