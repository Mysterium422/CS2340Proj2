"""
Tests for the root module
"""

from django.test import TestCase

from CS2340Proj2.validators import CustomPasswordValidator

class ValidateTests(TestCase):
    """
    Tests for the root module
    """
    def setUp(self):
        """
        Set up
        """
        self.validator = CustomPasswordValidator()

    def test_validate(self):
        """
        Test validate
        """
        self.validator.validate("password")

    def test_validate_short(self):
        """
        Test validate with a short password
        """
        with self.assertRaises(Exception):
            self.validator.validate("pass")

    def test_invalid(self):
        """
        Test invalid password
        """
        with self.assertRaises(Exception):
            self.validator.validate("pass word")

    def test_help_text(self):
        """
        Test help text
        """
        self.assertEqual(
            self.validator.get_help_text(),
            "Your password must be at least 6 characters long and must not contain spaces.")
