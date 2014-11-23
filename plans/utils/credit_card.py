# -*- coding: utf-8 -*-

import re
import calendar
import six

from datetime import datetime


class CardNotSupported(Exception):
    pass


class InvalidCard(Exception):
    pass


class RegExpError(Exception):
    pass


class CreditCard(object):
    """
    Class to represents the existing credit cards and validate it.
    """
    # regexp to validate the credit card number
    regexp = None
    card_name = None

    def __init__(self, name, number, cvv, year, month):
        self.name = name
        self.number = number
        self.cvv = cvv
        self.month = month
        self.year = year

    @property
    def iin(self):
        """
        Returns the IIN (Issuer Identification Number).
        """
        # In the most cases, this is the first six digits of the credit card
        # number
        raise NotImplementedError

    @property
    def masked_number(self):
        """
        Returns a masked number.
        """
        return six.u('%s******%s' % (self.number[:6], self.number[-4:]))

    def is_luhn_valid(self):
        """
        Checks if the credit card is valid using Luhn algorithm.
        """
        # See http://en.wikipedia.org/wiki/Luhn_algorithm
        try:
            digits = [int(d) for d in self.number]
        except ValueError:
            return False
        checksum = sum(digits[::-2] + [sum(divmod(d * 2, 10)) for d
                                       in digits[-2::-2]])
        return checksum % 10 == 0

    def _check_number(self):
        """
        Check if the credit card number is composed from digits.
        """
        try:
            int(self.number)
        except ValueError:
            return False
        return True

    def is_expired(self):
        "Checks if the card is expired or not."
        expired_date = datetime(self.year, self.month,
                                calendar.monthrange(self.year, self.month)[1])
        return datetime.today() > expired_date

    @classmethod
    def accept(cls, number):
        """
        Checks if the given number is accepted for this credit card type.
        """
        if not cls.regexp:
            raise RegExpError
        return bool(re.match(cls.regexp, number))

    def is_valid(self):
        """
        Checks if the card is valid.
        """
        return (self.is_luhn_valid() and self._check_number()
                and not self.is_expired())


class Visa(CreditCard):
    card_name = "Visa"
    regexp = re.compile("^4\d{12}(\d{3})?$")


class MasterCard(CreditCard):
    card_name = "MasterCard"
    regexp = re.compile("^(5[1-5]\d{4}|677189)\d{10}$")


class AmericanExpress(CreditCard):
    card_name = "Amex"
    regexp = re.compile("^3[47]\d{13}$")


class Discover(CreditCard):
    card_name = "Discover"
    regexp = re.compile("^(6011|65\d{2})\d{12}$")

cards = [Visa, MasterCard, AmericanExpress, Discover]
