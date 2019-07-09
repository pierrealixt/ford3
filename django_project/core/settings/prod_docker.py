
"""Configuration for production server."""
# noinspection PyUnresolvedReferences
from .prod import *  # noqa
import os
print(os.environ)

DEBUG = False

ALLOWED_HOSTS = ['*']

ADMINS = (
    ('Tim Sutton', 'tim@kartoza.com'),
    ('Christiaan van der Merwe', 'christiaan@kartoza.com'),
)
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ['DATABASE_NAME'],
        'USER': os.environ['DATABASE_USERNAME'],
        'PASSWORD': os.environ['DATABASE_PASSWORD'],
        'HOST': os.environ['DATABASE_HOST'],
        'PORT': 5432,
        'TEST': {
            'NAME': 'unittests',
        }
    }
}

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
MAIL_DOMAIN = os.getenv('MAIL_DOMAIN')
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')

EMAIL_HOST_USER = f'{SMTP_USER}@{MAIL_DOMAIN}'
EMAIL_HOST_PASSWORD = SMTP_PASSWORD
EMAIL_USE_TLS = False
EMAIL_SUBJECT_PREFIX = os.getenv('EMAIL_SUBJECT_PREFIX')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}

SITE_URL = os.getenv('SITEURL')
SERVER_PUBLIC_HOST = f'http://{SITE_URL}'
