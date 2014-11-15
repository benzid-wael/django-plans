# -*- coding: utf-8 -*-

from plans.utils.credit_card import CreditCard, Visa


visa_card = Visa("John Doe", "4111111111111111", "111", 2090, 12)
expired_visa = Visa("John Doe", "4111111111111111", "111", 1990, 12)
expired_card = CreditCard("John Doe", "4111111111111111", "111", 1990, 12)

unsupported_card = CreditCard("John Doe", "9991111111111111", "111", 1990, 12)
