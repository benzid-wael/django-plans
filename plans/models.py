# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import six

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from django_countries.fields import CountryField

from .conf import plan_settings


_logger = logging.getLogger("plans.models")


@python_2_unicode_compatible
class CreditCard(models.Model):
    """
    CreditCard model.
    """
    iin = models.CharField(_('IIN'), max_length=6, editable=False,
              help_text=_('The first 6 digits of the credit card number'))
    default = models.BooleanField(_('Default'), default=False, editable=False)
    card_type = models.CharField(_('Card Type'), max_length=20, editable=False)
    cardholder_name = models.CharField(max_length=40)
    ccn = models.CharField(_('CCN'), max_length=20)
    # TODO add a validator for the below field, and maybe a widget for the form
    expiration_date = models.CharField(_('Expiration date'), max_length=7,
            help_text=_('Expiration date should be in this format: MM/YYYY'))
    uid = models.CharField(_('UID'), max_length=20, blank=True, null=True,
            editable=False,
            help_text=_('A randomly generated UID by the billing gateway'))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '<%s: %s>' % (self.user.get_username(), self.iin)

    @property
    def masked_number(self):
        """
        Returns a masked number.
        """
        return six.u('%s******%s' % (self.iin[:6], self.iin[-4:]))


@python_2_unicode_compatible
class Plan(models.Model):
    """
    Plan model.
    """
    PERIOD_UNIT_CHOICES = (
        ("day", _("Day")),
        ("month", _("Month"))
    )
    name = models.CharField(_('Name'), max_length=30)
    plan_id = models.SlugField(max_length=20, editable=False)
    description = models.TextField(_('Description'), blank=True)
    active = models.BooleanField(_('Active'), default=False, db_index=True)
    default = models.BooleanField(_('Default'), default=False, db_index=True)
    trial_period = models.BooleanField(_('Trial Period'), default=False,
                                       help_text=_('Is there a trial period'))
    trial_period_amount = models.IntegerField(null=True)
    trial_period_unit = models.CharField(max_length=6, null=True,
                                         choices=PERIOD_UNIT_CHOICES)
    price = models.DecimalField(max_digits=7, decimal_places=2, db_index=True)
    currency = models.CharField(_('Currency'), max_length=3, default='EUR')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return six.u('%s' % self.name)

    @classmethod
    def get_default_plan(cls):
        """
        Returns the defined default plan in settings or the recent default plan.
        """
        if plan_settings.DEFAULT_PLAN:
            return plan_settings.DEFAULT_PLAN
        try:
            return cls.objects.filter(default=True).order_by('-pk')[0]
        except IndexError:
            return None


@python_2_unicode_compatible
class BillingInfo(models.Model):
    """
    Stores customer billing information.
    """
    user = models.OneToOneField(User, verbose_name=_('user'))
    tax_number = models.CharField(_('VAT'), max_length=200, blank=True, db_index=True)
    name = models.CharField(_('Name'), max_length=200, db_index=True)
    street = models.CharField(_('Street'), max_length=200)
    zipcode = models.CharField(_('Zip code'), max_length=200)
    city = models.CharField(_('City'), max_length=200)
    country = CountryField(_("Country"))

    # Shipping information
    # FIXME Should I move this info into another model
    shipping_name = models.CharField(_('Name (shipping)'), max_length=200, blank=True, help_text=_('optional'))
    shipping_street = models.CharField(_('Street (shipping)'), max_length=200, blank=True, help_text=_('optional'))
    shipping_zipcode = models.CharField(_('Zip code (shipping)'), max_length=200, blank=True, help_text=_('optional'))
    shipping_city = models.CharField(_('City (shipping)'), max_length=200, blank=True, help_text=_('optional'))

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_username()


@python_2_unicode_compatible
class UserVault(models.Model):
    """
    Stores User vaults.
    """
    user = models.ForeignKey(User, verbose_name=_('User'))
    # FIXME May be it's better to remove CreditCard, as we need only the 
    # vault_id.
    credit_card = models.OneToOneField(CreditCard, null=True,
                                       verbose_name=_('Credit Card'))
    vault_id = models.CharField(_('Vault ID'), max_length=64, unique=True)
    token = models.CharField(_('Token'), max_length=10, editable=False,
                help_text=_('A token generated by the gateway'))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def charge(self, amount):
        """
        Charges the users credit card, with he provided amount.
        """
        raise NotImplementedError


@python_2_unicode_compatible
class PaymentLog(models.Model):
    """
    Logging raw charges made to a users credit card.
    """
    vault = models.ForeignKey(UserVault, verbose_name=_('Vault'))
    transaction_id = models.CharField(max_length=128)
    amount = models.DecimalField(_('Amount'), max_digits=7, decimal_places=2)
    currency = models.CharField(_('Currency'), max_length=3, default='EUR')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            '%s charged %s %s - %s' % (self.user, self.amount,
                                       self.currency, self.transaction_id)
        )


@python_2_unicode_compatible
class Subscription(models.Model):
    PENDING, ACTIVE, PAST_DUE, EXPIRED, CANCELED = (
        "pending",
        "active",
        "past Due",
        "expired",
        "canceled",
    )
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (ACTIVE, 'Active'),
        (PAST_DUE, 'Past due'),
        (EXPIRED, 'Expired'),
        (CANCELED, 'Canceled')
    )
    subscription_id = models.CharField(_('Subscription'), max_length=10,
                                       unique=True)
    user_vault = models.ForeignKey(UserVault, verbose_name=_("User's vault"))
    plan = models.ForeignKey(Plan, verbose_name=_("Plan"))
    # Subscription state fields
    status = models.CharField(_('Status'), max_length=10, choices=STATUS_CHOICES)
    start_date = models.DateField(_('Start date'), default=datetime.now().date())
    next_billing_date = models.DateField(_('Next billing date'), editable=False)
    end_date = models.DateField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s: %s: %s" % (
            self.user_vault.user,
            self.subscription_id,
            self.status
        )

    def is_running(self):
        return (self.status in [Subscription.PENDING,
                                Subscription.ACTIVE,
                                Subscription.PAST_DUE])

    def cancel(self):
        """ Cancel this subscription instantly """
        raise NotImplementedError
