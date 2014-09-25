# -*- coding: utf-8 -*-

import re
import calendar

from datetime import datetime


class CardNotSupported(Exception):
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

    def is_luhn_valid(self):
        """
        Checks if the credit card is valid using Luhn algorithm.
        """
        # See http://en.wikipedia.org/wiki/Luhn_algorithm
        try:
            digits = [int(d) for d in self.number]
        except ValueError:
            return False
        checksum = sum(digits[::-2] + [sum(divmod(d * 2, 10)) for d \
                            in digits[-2::-2]])
        return checksum % 10 == 0

    def _checks_attrs(self):
        """
        Checks if the required attributes is given and not empty
        and the credit card number is composed from 16 digits.
        """
        try:
            int(self.number)
        except ValueError:
            return False
        return self.name and self.cvv and self.year and self.month

    def is_expired(self):
        "Checks if the card is expired or not."
        return (
            datetime.today() > datetime.date(self.year, self.month,
                                             calendar.monthrange(self.year,
                                                                 self.month)[1]
                                             )
        )

    @classmethod
    def check_number(cls, number):
        """
        Checks the credit number.
        """
        if not cls.regexp:
            raise RegExpError
        return bool(re.match(cls.regexp, number))

    def is_valid(self):
        """
        Checks if the card is valid.
        """
        return self.is_luhn_valid() and self._checks_attrs() and not \
                    self.is_expired()


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
