#!/usr/bin/env python
import sys

import django
from django.conf import settings

if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
        ),
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'tests',
            'django_nose',
        ),

        # Use nose to run all tests
        TEST_RUNNER = 'django_nose.NoseTestSuiteRunner',

        # Tell nose to measure coverage on the 'tests' app
        NOSE_ARGS = [
            '--with-coverage',
            # Erase previously collected coverage statistics before run
            '--cover-erase',
            '--cover-package=tests',
        ],
        SITE_ID=1,
        SECRET_KEY='this-is-just-for-tests',
    )

from django.test.utils import get_runner

def runtests():
    if hasattr(django, 'setup'):
        django.setup()
    apps = sys.argv[1:] or ['tests', ]
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(apps)
    sys.exit(failures)

if __name__ == '__main__':
    runtests()


