from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def validate(self, password, user=None):
        # Check if password is at least 6 characters long
        if len(password) < 6:
            raise ValidationError(
                _('Password must be at least 6 characters long.'),
                code='password_too_short',
            )
        
        # Check if password contains spaces
        if ' ' in password:
            raise ValidationError(
                _('Password cannot contain spaces.'),
                code='password_contains_spaces',
            )

    def get_help_text(self):
        return _(
            "Your password must be at least 6 characters long and must not contain spaces."
        )
