# -*- coding: utf-8 -*-
"""
Settings for plans application are all namespaced in PLANS setting.
For exemple:

    PLANS = {
        'DEFAULT_PLAN': 'plan_slug',
    }
"""

from django.conf import settings


USER_SETTINGS = getattr(settings, "PLANS", None)

DEFAULT_SETTINGS = {
    "DEFAULT_PLAN": None,
}


class Settings(object):
    """
    A settings object that allows us to access to all settings as properties.
    """
    def __init__(self, user_settings, default_settings):
        self.user_settings = user_settings or {}
        self.default_settings = default_settings or {}

    def __getattr__(self, attr):
        val = self.user_settings.get(attr, self.default_settings[attr])
        # Cache the result
        setattr(self, attr, val)
        return val


plan_settings = Settings(USER_SETTINGS, DEFAULT_SETTINGS)
