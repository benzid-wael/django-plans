# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Plan(models.Model):
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

    def __unicode__(self):
        return u'%s' % self.name

    @classmethod
    def get_default_plan(cls):
        """
        Returns the recent default plan.
        """
        try:
            return cls.objects.filter(default=True).order_by('-pk')[0]
        except IndexError:
            return None


