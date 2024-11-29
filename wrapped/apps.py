"""
App configuration for wrapped view
"""

from django.apps import AppConfig

class SpotifyConfig(AppConfig):
    """
    Configuration for the wrapped view
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wrapped'
