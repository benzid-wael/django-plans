# -*- coding: utf-8 -*-
import braintree
import six

from plans.utils.credit_card import (
    InvalidCard, CreditCard, Visa, MasterCard, AmericanExpress, Discover
)
from .base import Gateway, GatewayNotConfigured


class BraintreeGateway(Gateway):

    """
    Braintree Payements Gateway class.
    """

    name = "Braintree Payments"
    default_currency = "USD"
    supported_card_types = [Visa, MasterCard, AmericanExpress, Discover]

    def __init__(self, **kwargs):
        # TODO this need to be executed only when server start.
        test_mode = kwargs.pop("test_mode", False)
        gateway_settings = kwargs.pop("gateway_settings", {})
        if test_mode:
            env = braintree.Environment.Sandbox
        else:
            env = braintree.Environment.Production
        if (not gateway_settings
                or not gateway_settings.get("MERCHANT_ACCOUNT_ID")
                or not gateway_settings.get("PUBLIC_KEY")
                or not gateway_settings.get("PRIVATE_KEY")):
            raise GatewayNotConfigured("'%s' gateway is not correctly "
                                       "configured." % self.name)
        braintree.Configuration.configure(
            env,
            gateway_settings['MERCHANT_ACCOUNT_ID'],
            gateway_settings['PUBLIC_KEY'],
            gateway_settings['PRIVATE_KEY']
        )

    def get_transaction(self, transaction_id):
        """Return the transaction with the given ID if exists, else None"""
        return braintree.Transaction.find(str(transaction_id))

    def _build_errors(self, response, transaction=None, debug=False):
        if response.is_success:
            return None
        result = {
            "errors": [error.message for error in response.errors.deep_errors]
        }
        if response.transaction:
            transaction = response.transaction
        transaction_fields = {
            "processor_declined": [
                "processor_response_code", "processor_response_text"
            ],
            "gateway_rejected": ["gateway_rejection_reason"]
        }
        if transaction:
            fields = transaction_fields.get(transaction.status, [])
            result["transaction"] = {
                "status": transaction.status
            }
            result["transaction"].update({
                field: getattr(transaction, field) for field in fields
            })
        return result

    def _build_request(self, options=None):
        """Build braintree request from options."""
        request = {}
        options = options or {}
        if options.get("customer", None):
            request.update({
                "customer": {
                    "first_name": options["customer"].get("first_name", ""),
                    "last_name": options["customer"].get("last_name", ""),
                    "company": options["customer"].get("company", ""),
                    "phone": options["customer"].get("phone", ""),
                    "fax": options["customer"].get("fax", ""),
                    "website": options["customer"].get("website", ""),
                    "email": options["customer"].get("email", "")
                }
            })
        # billing address
        # shipping address
        return request

    def charge(self, credit_card, amount, options=None):
        try:
            is_valid = (isinstance(credit_card, CreditCard)
                        and self.validate(credit_card))
        except Exception as e:
            raise InvalidCard(six.text_type(e))

        if not is_valid:
            # TODO inject an `_error` attribute if the credit card is invalid
            raise InvalidCard()

        request = self._build_request(options)

        request["amount"] = amount
        request["credit_card"] = {
            "number": credit_card.number,
            "cardholder_name": credit_card.name,
            "expiration_date": credit_card.expiration_date,
            "cvv": credit_card.cvv
        }

        # Submitting transaction for settlement
        request["options"] = {
            "submit_for_settlement": True
        }

        # Send request to braintree
        response = braintree.Transaction.sale(request)
        status = "success" if response.is_success else "failure"
        result = {
            "status": status,
        }
        if response.is_success:
            result["transaction"] = {
                "id": response.transaction.id,
                "status": str(response.transaction.status)
            }
        result.update(self._build_errors(response) or {})
        return result

    def refund(self, transaction_id, amount=None):
        transaction = self.get_transaction(str(transaction_id))
        if not transaction:
            raise ValueError("Bad transaction ID {}".format(transaction_id))
        response = braintree.Transaction.refund(str(transaction_id), amount)
        status = "success" if response.is_success else "failure"
        result = {
            "status": status,
            "transaction": {
                "status": transaction.status
            }
        }
        result.update(self._build_errors(response, transaction) or {})
        return result
