# -*- coding: utf-8 -*-

from django.test import TestCase

from plans.utils.credit_card import CreditCard, Visa
from tests import credit_card


class CreditCardTestCase(TestCase):
    def setUp(self):
        self.creditcard_data = {
            "name": "John Doe",
            "number": "4111111111111111",
            "cvv": "111",
            "year": 2022,
            "month": 12
        }
        self.creditcard = CreditCard(**self.creditcard_data)

    def test_non_expired_creditcard(self):
        res = self.creditcard.is_expired()
        self.assertEqual(res, False)

    def test_expired_creditcard(self):
        creditcard = credit_card.expired_card
        res = creditcard.is_expired()
        self.assertEqual(res, True)

    def test_good_ccn(self):
        res = self.creditcard._check_number()
        self.assertEqual(res, True)

    def test_bad_ccn(self):
        creditcard = CreditCard("John Doe", "abcd", "111", 2022, 1)
        res = creditcard._check_number()
        self.assertEqual(res, False)

    def test_luhn_valid_creditcard(self):
        res = self.creditcard.is_luhn_valid()
        self.assertEqual(res, True)

    def test_non_luhn_valid_creditcard(self):
        creditcard = CreditCard("John Doe", "4111123111111111", "111", 2022,
                                12)
        res = creditcard.is_luhn_valid()
        self.assertEqual(res, False)

    def test_valid_creditcard(self):
        res = self.creditcard.is_valid()
        self.assertEqual(res, True)

    def test_non_valid_creditcard(self):
        bad_creditcards = [
            CreditCard("John Doe", "4111111111111111", "111", 1990, 12),
            CreditCard("John Doe", "abcd", "111", 2022, 1),
            CreditCard("John Doe", "4111123111111111", "111", 2022, 12)
        ]
        res = any([cc.is_valid() for cc in bad_creditcards])
        self.assertEqual(res, False)

    def test_valid_visa(self):
        self.assertEqual(Visa.accept(self.creditcard_data['number']), True)

    def test_invalid_visa(self):
        self.assertEqual(Visa.accept("11111"), False)
        self.assertEqual(Visa.accept("1111111111111111"), False)
