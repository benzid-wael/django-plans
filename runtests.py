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

        # Plans settings
        PLANS={
            "DEFAULT_PLAN": "Tester",
            "BILLING_GATEWAY": (
                "plans.gateway.braintree_payements.BraintreeGateway"
            ),
            "GATEWAY_SETTINGS": {
                "MERCHANT_ACCOUNT_ID": "944fcnns6fsgdgv6",
                "PUBLIC_KEY": "8bwvnx4hh2r8j45n",
                "PRIVATE_KEY": "7839eaa9478072e88d48e89f43210b1c"
            },
            "TEST_MODE": True,
            "STORE_CUSTOMER_INFO": False,
            "TAXATION_POLICY": "plans.taxation.EUTaxationPolicy",
            "TAX_PERCENT": "10",  # Tax is 10%
        },

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
    apps = sys.argv[1:] or ['tests']
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(apps)
    sys.exit(failures)

if __name__ == '__main__':
    runtests()
