"""
Module for the forms used in the accounts app
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    """
    User Creation Form with optional email field
    """
    email = forms.EmailField(label="Email (Optional)", required=False)
    usable_password = None

    class Meta:
        """
        Form Meta Class
        """
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }


    def save(self, commit=True):
        """
        Save form method
        """
        user = super().save(commit=False)
        # Set the optional email field
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean_email(self):
        """
        Clean email method
        """
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email
