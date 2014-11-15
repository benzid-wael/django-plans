# -*- coding: utf-8 -*-

from nose.tools import raises

from django.test import TestCase

from plans.gateway.base import Gateway
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
