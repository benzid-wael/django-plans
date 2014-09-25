# -*- coding: utf-8 -*-

from .utils.credit_card import CardNotSupported


class Gateway(object):
    """
    Base class for all billing gateways.
    """
    name = None
    default_currency = None
    # list of supported card types
    supported_card_types = []

    def validate(self, credit_card):
        """
        Validate the given credit card if it's supported,
        else raise CardNotSupported error.
        """
        is_supported = False
        for card_type in self.supported_card_types:
            if card_type.check_number(credit_card.number):
                credit_card.card_type = card_type
                is_supported = True
                break
        if not is_supported:
            raise CardNotSupported("Credit card is not supported by the {0} "
                                   "gateway".format(self.name))
        # Check if credit card is valid
        return credit_card.is_valid()

    def charge(self, credit_card, amount, options=None):
        """
        Charges the credit card with the provided amount.
        """
        raise NotImplementedError

    def refund(self, transaction_id, amount=None):
        """
        Refund transaction with the given ID. If amount is provided,
        refund only portion of the transaction.
        """
        raise NotImplementedError

    def void(self, transaction_id):
        """
        Void transaction if it's authorized or submitted_for_settlement.
        """
        raise NotImplementedError

    def subscribe(self, credit_card, options=None):
        """
        Subscribe customer
        """
        raise NotImplementedError

    def unsubscribe(self, credit_card, options=None):
        """
        Unsubscribe customer
        """
        raise NotImplementedError

    def store(self, credit_card, options=None):
        """
        Store the credit card and customer information on the gateway.
        """
        raise NotImplementedError

    def unstore(self, credit_card, options=None):
        """
        Store the credit card and customer information on the gateway.
        """
        raise NotImplementedError
