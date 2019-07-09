from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from ford3.tokens import account_activation_token


class Notifier:
    @classmethod
    def send_activation_email(self, user):
        subject = '[OpenEdu] Account activation'
        message = render_to_string(
            'emails/account_activation.html', {
                'user': user,
                'domain': settings.SERVER_PUBLIC_HOST,
                'valid_link_days': settings.VALID_LINK_DAYS,
                'uid': urlsafe_base64_encode(
                    force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
        user.email_user(subject, message)
