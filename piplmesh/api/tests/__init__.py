import os

from django.utils import unittest

def suite():
    return unittest.TestSuite((
        unittest.TestLoader().discover(os.path.abspath(os.path.dirname(__file__))),
        ))
