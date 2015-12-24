# -*- coding: utf-8 -*-
"""Tests for _Mail class."""

# from python_utils.helper import _Helper
# from python_utils import helper

import unittest
from python_utils.helper import _Helper


class TestMailPythonUtils(unittest.TestCase):
    """Add documentation here."""

    def setUp(self):
        """Add documentation here."""
        self.helper = _Helper()

    def tearDown(self):
        """Add documentation here."""
        del self.helper

    def test__1_add_section(self):
        """Add documentation here."""
        self.helper.add_section_name("TESTE")
        print self.helper.name
