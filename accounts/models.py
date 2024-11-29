"""
Models for the accounts app
"""

from django.db import models
from django.contrib.auth.models import User


class SpotifyToken(models.Model):
    """
    Model for spotify token
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)

    def __str__(self):
        """
        To String method
        """
        return f"SpotifyToken for {self.user.username}"
