# -*- coding: utf-8 -*-

from nose.tools import raises

from django.test import TestCase

from plans.gateway.base import Gateway
from plans.conf import (
    Settings, DEFAULT_SETTINGS, IMPORT_STRINGS, NotFoundAttribute
)


TEST_USER_SETTINGS = {
    "DEFAULT_PLAN": "default_plan_name",
    "BILLING_GATEWAY": "tests.test_conf.BillingGateway",
    "TEST_MODE": False,
    "STORE_CUSTOMER_INFO": False,
    "TAXATION_POLICY": "plans.taxation.EUTaxationPolicy",
    "TAX_PERCENT": 10,
}


class BadGateway(object):
    pass


class BillingGateway(Gateway):
    pass


class SettingsTests(TestCase):
    """Basic tests for Settings class."""
    def setUp(self):
        self.settings = Settings(TEST_USER_SETTINGS, DEFAULT_SETTINGS,
                                 IMPORT_STRINGS)

    @raises(NotFoundAttribute)
    def test_undefiend_setting(self):
        self.settings.undefinedSetting

    def test_getattr(self):
        expected = "django-plans"
        test_user_setting = {
            "APP_NAME": expected
        }
        setting = Settings(test_user_setting, DEFAULT_SETTINGS, {})
        app_name = setting.APP_NAME
        self.assertEqual(app_name, expected)
