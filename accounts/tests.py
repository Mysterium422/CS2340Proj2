"""
Tests For the account app
"""

from django.test import TestCase, Client
from accounts.forms import CustomUserCreationForm

# Create your tests here.


class CreationFormTests(TestCase):
    """
    Tests for the creation form
    """

    def test_invalid_form(self):
        """
        Test invalid form
        """
        form_data = {
            'username': 'test',
            'password1': 'test',
            'password2': 'test',
            'email': ' ',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_form(self):
        """
        Test valid form
        """
        form_data = {
            'username': 'test1',
            'password1': 'strongpassword1',
            'password2': 'strongpassword1',
            'email': 'test@test.com'
        }

        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_username_already_in_use(self):
        """
        Test form submission with an already-used username
        """
        form_data = {
            'username': 'test2',
            'password1': 'strongpassword2',
            'password2': 'strongpassword2',
            'email': 'test@test.com'
        }

        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        form.save()

        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_email_already_in_use(self):
        """
        Test form submission with already used username
        """
        form_data = {
            'username': 'test2',
            'password1': 'strongpassword2',
            'password2': 'strongpassword2',
            'email': 'test@test.com'
        }

        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        form.save()

        form_data = {
            'username': 'test3',
            'password1': 'strongpassword2',
            'password2': 'strongpassword2',
            'email': 'test@test.com'
        }

        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

class ViewTestCases(TestCase):
    """
    Test cases for the views
    """

    def setUp(self):
        """
        Set up the client
        """
        self.client = Client()

    def test_sign_up(self):
        """
        Test sign-up page
        """
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')
