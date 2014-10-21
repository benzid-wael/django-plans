# -*- coding: utf-8 -*-
"""
Settings for plans application are all namespaced in PLANS setting.
For exemple:

    PLANS = {
        "DEFAULT_PLAN": "plan_name",
        "BILLING_GATEWAY": "plans.gateway.BraintreeGateway",
        "TEST_MODE": False,
        "STORE_CUSTOMER_INFO": False,
        "TAXATION_POLICY": "plans.taxation.EUTaxationPolicy",
        "TAX_PERCENT": "10", # Tax is 10%
    }
"""

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from utils.loader import load_class
from gateway.base import Gateway


USER_SETTINGS = getattr(settings, "PLANS", None)

DEFAULT_SETTINGS = {
    "DEFAULT_PLAN": None,
    "TEST_MODE": False,
    "STORE_CUSTOMER_INFO": True,
    "TAX_PERCENT": 0,
}


class NotFoundAttribute(Exception):
    pass


class Settings(object):
    """
    A settings object that allows us to access to all settings as properties.
    """
    def __init__(self, user_settings, default_settings):
        self.user_settings = user_settings or {}
        self.default_settings = default_settings or {}

    def _check_gateway(self):
        """
        Check if the provided gateway is valid:
        1) the gateway is required and should be a class
        2) the gateway should inherits from the Gateway base class
        """
        try:
            self.gateway = load_class(self.BILLING_GATEWAY)
        except NotFoundAttribute:
            raise ImproperlyConfigured("No billing gateway specified in your "
                                       "settings.")
        except ImportError:
            raise ImproperlyConfigured("Missing gateway: %s" % (
                                            self.BILLING_GATEWAY
                                      )
            )
        # check if the gateway inherits from the Gateway abstract class
        assert isinstance(self.gateway, Gateway)

    def _check_tax_percent(self):
        """Check the value of TAX_PERCENT setting"""
        assert 0 <= self.TAX_PERCENT <= 100

    def _check_tax_policy(self):
        """Check TAXATION_POLICY setting"""
        if self.TAXATION_POLICY:
            try:
                self.tax_policy = load_class(self.TAXATION_POLICY)
            except ImportError:
                raise ImproperlyConfigured("Missing taxation policy: %s" % (
                                                self.TAXATION_POLICY
                                          )
                )

    def __getattr__(self, attr):
        if attr not in self.default_settings.keys():
            raise NotFoundAttribute
        val = self.user_settings.get(attr, self.default_settings[attr])
        # Cache the result
        setattr(self, attr, val)
        return val


plan_settings = Settings(USER_SETTINGS, DEFAULT_SETTINGS)
