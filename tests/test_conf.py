# -*- coding: utf-8 -*-

from nose.tools import raises

from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured

from plans.gateway.base import Gateway
from plans.conf import Settings, DEFAULT_SETTINGS, NotFoundAttribute


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
        self.settings = Settings(TEST_USER_SETTINGS, DEFAULT_SETTINGS)

    @raises(NotFoundAttribute)
    def test_undefiend_setting(self):
        self.settings.undefinedSetting

    @raises(ImproperlyConfigured)
    def test_undefined_gateway(self):
        bad_setting = Settings({}, DEFAULT_SETTINGS)
        bad_setting._check_gateway()

    @raises(ImproperlyConfigured)
    def test_notfound_gateway(self):
        test_user_setting = {
            "BILLING_GATEWAY": "app.gateway.NotDefined"
        }
        bad_setting = Settings(test_user_setting, DEFAULT_SETTINGS)
        bad_setting._check_gateway()

    @raises(AssertionError)
    def test_gateway_api(self):
        """Verify if the specified gateway inherits from the Gateway class"""
        test_user_setting = {
            "BILLING_GATEWAY": "tests.test_conf.BadGateway"
        }
        bad_setting = Settings(test_user_setting, DEFAULT_SETTINGS)
        bad_setting._check_gateway()

    def test_good_gateway(self):
        test_user_setting = {
            "BILLING_GATEWAY": "tests.test_conf.BillingGateway"
        }
        setting = Settings(test_user_setting, DEFAULT_SETTINGS)
        ret = setting._check_gateway()
        # test does not raises any exception
        self.assertEqual(ret, None)

    def test_getattr(self):
        expected = "django-plans"
        test_user_setting = {
            "APP_NAME": expected
        }
        setting = Settings(test_user_setting, DEFAULT_SETTINGS)
        app_name = setting.APP_NAME
        self.assertEqual(app_name, expected)
