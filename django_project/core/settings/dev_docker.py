from .dev import *  # noqa
import os # noqa

SECRET_KEY = '*fneknn-)l-b+6muz(d*z#$7ng_(kxkxf)9a65f(ewbiwqmmj$'

ALLOWED_HOSTS = ['*',
                 u'0.0.0.0']

ADMINS = ()

# Set debug to True for development
DEBUG = True
TEMPLATE_DEBUG = DEBUG
LOGGING_OUTPUT_ENABLED = DEBUG
LOGGING_LOG_SQL = DEBUG
CRISPY_FAIL_SILENTLY = not DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'gis',
        'USER': 'docker',
        'PASSWORD': 'docker',
        'HOST': 'db',
        'PORT': 5432,
        'TEST': {
            'NAME': 'unittests',
        }
    }
}

PIPELINE_ENABLED = False
STATICFILES_STORAGE = 'pipeline.storage.NonPackagingPipelineStorage'
SERVER_PUBLIC_HOST = 'http://localhost'
