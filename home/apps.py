"""
App Configuration for home
"""

from django.apps import AppConfig

class SpotifyConfig(AppConfig):
    """
    Spotify App Configuration
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'
