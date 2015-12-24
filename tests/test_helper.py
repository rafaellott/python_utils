# -*- coding: utf-8 -*-
"""Tests for _Helper class."""

# from python_utils.helper import _Helper
# from python_utils import helper

import unittest
from python_utils.django_emails import _Mail


class TestPythonUtils(unittest.TestCase):
    """Add documentation here."""

    def setUp(self):
        """Add documentation here."""
        pass

    def tearDown(self):
        """Add documentation here."""
        pass

    def test__1_send_newsletter(self):
        """Add documentation here."""
        mail = _Mail(
            recipient_list=['rafaellott.2@gmail.com'],
            subject="Teste newsletter", sender="test@localhost",
            fail_silently=False,
            base_url="https://github.com/rafaellott/python_utils"
        )
        mail.send_newsletter()
