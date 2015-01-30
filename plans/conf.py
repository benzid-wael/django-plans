# -*- coding: utf-8 -*-
"""
Settings for plans application are all namespaced in PLANS setting.
For exemple:

PLANS = {
    "DEFAULT_PLAN": "plan_name",
    "BILLING_GATEWAY": "plans.gateway.braintree_payements.BraintreeGateway",
    "GATEWAY_SETTINGS": {
        "MERCHANT_ACCOUNT_ID": "your_merchant_account_id",
        "PUBLIC_KEY": "your_public_key",
        "PRIVATE_KEY": "your_private_key"
    },
    "TEST_MODE": False,
    "STORE_CUSTOMER_INFO": False,
    "TAXATION_POLICY": "plans.taxation.EUTaxationPolicy",
    "TAX_PERCENT": "10", # Tax is 10%
}
"""

from django.conf import settings

from plans.utils.loader import load_class


USER_SETTINGS = getattr(settings, "PLANS", None)

DEFAULT_SETTINGS = {
    "DEFAULT_PLAN": None,
    "TEST_MODE": False,
    "STORE_CUSTOMER_INFO": True,
    "TAX_PERCENT": 0,
}

IMPORT_STRINGS = (
    "BILLING_GATEWAY",
    "TAXATION_POLICY"
)


class NotFoundAttribute(Exception):
    pass


class Settings(object):

    """
    A settings object that allows us to access to all settings as properties.
    """

    def __init__(self, user_settings, default_settings, import_strings):
        self.user_settings = user_settings or {}
        self.default_settings = default_settings or {}
        self.import_strings = import_strings or ()

    def __getattr__(self, attr):
        try:
            val = self.user_settings[attr]
        except KeyError:
            if attr in self.default_settings.keys():
                val = self.default_settings[attr]
            else:
                raise NotFoundAttribute

        # check if the value should be imported
        if val and attr in self.import_strings:
            val = load_class(val)

        # Cache the result
        setattr(self, attr, val)
        return val


plan_settings = Settings(USER_SETTINGS, DEFAULT_SETTINGS, IMPORT_STRINGS)
