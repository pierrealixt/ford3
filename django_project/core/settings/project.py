import os  # noqa
from distutils.util import strtobool

from django.utils.translation import ugettext_lazy as _
from .contrib import *  # noqa


# Project apps
INSTALLED_APPS += (
    'base',
    'ford3',
)

# Due to profile page does not available,
# this will redirect to home page after login
LOGIN_REDIRECT_URL = '/'

# How many versions to list in each project box
PROJECT_VERSION_LIST_SIZE = 10

# Set debug to false for production
DEBUG = TEMPLATE_DEBUG = False

SOUTH_TESTS_MIGRATE = False


# Set languages which want to be translated
LANGUAGES = (
    ('en', _('English')),
)

# Set storage path for the translation files
LOCALE_PATHS = (absolute_path('locale'),)


MIDDLEWARE = [
    # Add any custome middleware classes here
] + MIDDLEWARE

# Project specific javascript files to be pipelined
# For third party libs like jquery should go in contrib.py

PIPELINE['JAVASCRIPT']['project'] = {
    'source_filenames': (
        'js/csrf-ajax.js',
        'js/ford3.js',
    ),
    'output_filename': 'js/project.js',
}

# Project specific css files to be pipelined
# For third party libs like bootstrap should go in contrib.py
PIPELINE['STYLESHEETS']['project'] = {
    'source_filenames': (
        'css/ford3.css',
        'css/form.css',
        'css/stylesheet.css',
    ),
    'output_filename': 'css/project.css',
    'extra_context': {
        'media': 'screen, projection',
    },
}

STATIC_URL = '/static/'


# Selenium test configuration
# URL of selenium driver. example: http://hub.test:4444/wd/hub
SELENIUM_DRIVER = os.environ.get('SELENIUM_DRIVER', '')

SELENIUM_UNIT_TEST_FLAG = strtobool(
    os.environ.get('SELENIUM_UNIT_TEST_FLAG', 'False'))

SELENIUM_TEST_HOSTNAME = os.environ.get('SELENIUM_TEST_HOSTNAME', 'localhost')
SELENIUM_TEST_PORT = int(os.environ.get('SELENIUM_TEST_PORT', '0'))
