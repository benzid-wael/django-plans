# -*- coding: utf-8 -*-
import braintree

from plans.utils.credit_card import Visa, MasterCard, AmericanExpress, Discover
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
