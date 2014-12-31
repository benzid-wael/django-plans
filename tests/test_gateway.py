# -*- coding: utf-8 -*-

from nose.tools import raises

from django.test import TestCase

from plans.conf import plan_settings
from plans.gateway.base import Gateway
from plans.gateway.braintree_payments_gateway import BraintreeGateway
from plans.utils import credit_card

from tests.credit_card import (
    visa_card,
    expired_visa,
    unsupported_card,
    bad_cvv
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

    """
    General tests for Braintree gateway.
    """

    def setUp(self):
        self.gateway = BraintreeGateway(test_mode=plan_settings.TEST_MODE,
                                        gateway_settings=(
                                            plan_settings.GATEWAY_SETTINGS
                                        ))

    def test_gateway_initialisation(self):
        import braintree
        is_sandbox = (
            "sandbox" in
            braintree.Configuration.environment._Environment__auth_url
        )
        self.assertEqual(is_sandbox, True)

    def test_card_type(self):
        self.gateway.validate(visa_card)
        self.assertEqual(visa_card.card_type, credit_card.Visa)

    def test_validate_visa_card(self):
        ret = self.gateway.validate(visa_card)
        self.assertTrue(ret)

    def test_charge_success(self):
        response = self.gateway.charge(visa_card, 100)
        self.assertEqual(response['status'], "success")

    @raises(credit_card.InvalidCard)
    def test_charge_expired_card_fail(self):
        self.gateway.charge(expired_visa, 100)

    @raises(credit_card.InvalidCard)
    def test_charge_unsupported_fail(self):
        self.gateway.charge(unsupported_card, 100)

    def test_charge_bad_cvv_fail(self):
        response = self.gateway.charge(bad_cvv, 100)
        self.assertEqual(response['status'], "failure")
        msg = (
            "CVV must be 4 digits for American Express and 3 digits for "
            "other card types."
        )
        self.assertEqual(response["response"].message, msg)
