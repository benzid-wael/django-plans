# -*- coding: utf-8 -*-

from nose.tools import raises

from django.test import TestCase

from plans.conf import Settings
from plans.gateway.base import Gateway
from plans.gateway.braintree_payments_gateway import BraintreeGateway
from plans.utils import credit_card

from tests.credit_card import (
    visa_card,
    expired_visa,
    unsupported_card
)


class SampleGateway(Gateway):

    name = "Sample Gateway"
    default_currency = "TND"
    supported_card_types = [
        credit_card.Visa,
        credit_card.MasterCard,
    ]


class GatewayTests(TestCase):

    """Basic tests for Gateway class"""

    def setUp(self):
        self.gateway = SampleGateway()

    def test_support_visa(self):
        self.assertEqual(self.gateway.validate(visa_card), True)

    def test_validate_expired_visa(self):
        self.assertEqual(self.gateway.validate(expired_visa), False)

    @raises(credit_card.CardNotSupported)
    def test_unsupported_card(self):
        self.gateway.validate(unsupported_card)


class BraintreeGatewayTests(TestCase):
    def setUp(self):
        test_user_settings = {
            "DEFAULT_PLAN": "plan_name",
            "BILLING_GATEWAY": (
                "plans.gateway.braintree_payements.BraintreeGateway"
            ),
            "GATEWAY_SETTINGS": {
                "MERCHANT_ACCOUNT_ID": "your_merchant_account_id",
                "PUBLIC_KEY": "your_public_key",
                "PRIVATE_KEY": "your_private_key"
            },
            "TEST_MODE": True,
            "STORE_CUSTOMER_INFO": False,
        }
        settings = Settings(test_user_settings, {})
        self.gateway = BraintreeGateway(test_mode=settings.TEST_MODE,
                                        gateway_settings=(
                                            settings.GATEWAY_SETTINGS
                                        ))

    def test_gateway_initialisation(self):
        import braintree
        is_sandbox = (
            "sandbox" in
            braintree.Configuration.environment._Environment__auth_url
        )
        self.assertEqual(is_sandbox, True)
