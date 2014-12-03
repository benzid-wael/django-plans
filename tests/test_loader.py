# -*- coding: utf-8 -*-

from nose.tools import raises

from django.test import TestCase

from plans.utils.loader import load_class


class SomeClass(object):
    pass


class LoaderTests(TestCase):

    def test_load_class_success(self):
        cls = load_class("tests.test_loader.SomeClass")
        instance = cls()
        self.assertTrue(isinstance(instance, SomeClass))

    @raises(ImportError)
    def test_load_class_failed(self):
        load_class("plans.not_here.DoesNotExist")
