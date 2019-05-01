import os
import sys

import django
from django.conf import settings
from django.test.runner import DiscoverRunner


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

DEFAULT_SETTINGS = dict(
    ROOT_URLCONF='tests.urls',
    SECRET_KEY="38dh*skf8sjfhs287dh&^hd8&3hdg*j2&sd",
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'rest_framework_bulk.sqlite',
        }
    },
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.staticfiles',
        'rest_framework',
        'tests'
    ]
)


def run_tests():
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)
    django.setup()
    failures = DiscoverRunner(failfast=False).run_tests(['tests'])
    sys.exit(bool(failures))


if __name__ == '__main__':
    run_tests()
