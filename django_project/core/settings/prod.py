# coding=utf-8

"""Project level settings."""
from .project import *  # noqa
import os


if 'SENTRY_KEY' in os.environ:
    SENTRY_KEY = os.environ['SENTRY_KEY']
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    sentry_sdk.init(
        dsn=SENTRY_KEY,
        integrations=[DjangoIntegration()],
        send_default_pii=True
    )

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
# Localhost:9000 for vagrant
# Changes for live site
# ['*'] for testing but not for production

ALLOWED_HOSTS = [
    'localhost:8080',
    'ford3.kartoza.com']

# Pipeline - for production we want to compress resources
# PIPELINE['JS_COMPRESSOR'] = 'pipeline.compressors.yuglify.YuglifyCompressor'
# PIPELINE['CSS_COMPRESSOR'] = 'pipeline.compressors.yuglify.YuglifyCompressor'
PIPELINE['PIPELINE_ENABLED'] = False

# Comment if you are not running behind proxy
USE_X_FORWARDED_HOST = True

# Set debug to false for production
DEBUG = TEMPLATE_DEBUG = False

SERVER_EMAIL = 'no_reply@openedu.org.za'
EMAIL_HOST = 'kartoza.com'
DEFAULT_FROM_EMAIL = 'no_reply@openedu.org.za'
