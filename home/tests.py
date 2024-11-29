"""
Tests for the Spotify API
"""

from django.test import TestCase
from django.contrib.auth.models import User

from home.test.spotify_api_test import testSpotifyAPI
from home.spotify_api import create_wrapped
# Create your tests here.

class SpotifyAPITests(TestCase):
    """
    Tests for the Spotify API
    """

    def setUp(self):
        """
        Set up mock Spotify API
        """
        self.spotify_api = testSpotifyAPI()

    def test_create_wrapped(self):
        """
        Test Create Wrapped
        """
        test_user = None
        if User.objects.filter(username='test').exists():
            test_user = User.objects.get(username='test')
        else:
            test_user = User.objects.create_user(username='test', password='test')

        wrapped = create_wrapped(test_user, self.spotify_api)

        self.assertEqual(wrapped.top_weekly_artists.filter(topweeklyartistrel__rank=1)[0].name,
                         "Linkin Park")
        self.assertEqual(wrapped.top_weekly_artists.filter(topweeklyartistrel__rank=2)[0].name,
                         "My Chemical Romance")
        self.assertEqual(wrapped.top_weekly_artists.filter(topweeklyartistrel__rank=3)[0].name,
                         "結束バンド")
        self.assertEqual(wrapped.top_weekly_artists.filter(topweeklyartistrel__rank=4)[0].name,
                         "Sayuri")
        self.assertEqual(wrapped.top_weekly_artists.filter(topweeklyartistrel__rank=5)[0].name,
                         "TesseracT")

        self.assertEqual(wrapped.top_artists.filter(topartistrel__rank=1)[0].name,
                         "Dance Gavin Dance")
        self.assertEqual(wrapped.top_artists.filter(topartistrel__rank=2)[0].name,
                         "Polyphia")
        self.assertEqual(wrapped.top_artists.filter(topartistrel__rank=3)[0].name,
                         "結束バンド")
        self.assertEqual(wrapped.top_artists.filter(topartistrel__rank=4)[0].name,
                         "TesseracT")
        self.assertEqual(wrapped.top_artists.filter(topartistrel__rank=5)[0].name,
                         "YOASOBI")

        self.assertEqual(wrapped.top_weekly_songs.filter(topweeklysongrel__rank=1)[0].name,
                         "Chucky vs. The Giant Tortoise")
        self.assertEqual(wrapped.top_weekly_songs.filter(topweeklysongrel__rank=1)[0].album,
                         "Mothership")
        self.assertEqual(wrapped.top_weekly_songs.filter(topweeklysongrel__rank=1)[0].artist_name,
                         "Dance Gavin Dance")

        self.assertEqual(wrapped.top_weekly_songs.filter(topweeklysongrel__rank=2)[0].name,
                         "Livin' On A Prayer")
        self.assertEqual(wrapped.top_weekly_songs.filter(topweeklysongrel__rank=2)[0].album,
                         "Slippery When Wet")
        self.assertEqual(wrapped.top_weekly_songs.filter(topweeklysongrel__rank=2)[0].artist_name,
                         "Bon Jovi")

        self.assertEqual(wrapped.top_weekly_songs.filter(topweeklysongrel__rank=3)[0].name,
                         "Chromatic Aberration")
        self.assertEqual(wrapped.top_weekly_songs.filter(topweeklysongrel__rank=3)[0].album,
                         "Quiet World")
        self.assertEqual(wrapped.top_weekly_songs.filter(topweeklysongrel__rank=3)[0].artist_name,
                         "Native Construct")

        self.assertEqual(wrapped.top_weekly_songs.filter(topweeklysongrel__rank=4)[0].name,
                         "unravel")
        self.assertEqual(wrapped.top_weekly_songs.filter(topweeklysongrel__rank=4)[0].album,
                         "unravel")
        self.assertEqual(wrapped.top_weekly_songs.filter(topweeklysongrel__rank=4)[0].artist_name,
                         "Ado")

        self.assertEqual(wrapped.top_weekly_songs.filter(topweeklysongrel__rank=5)[0].name,
                         "MUKANJYO")
        self.assertEqual(wrapped.top_weekly_songs.filter(topweeklysongrel__rank=5)[0].album,
                         "MUKANJYO")
        self.assertEqual(wrapped.top_weekly_songs.filter(topweeklysongrel__rank=5)[0].artist_name,
                         "Survive Said The Prophet")

        self.assertEqual(wrapped.top_songs.filter(topsongrel__rank=1)[0].name,
                         "ギターと孤独と蒼い惑星")
        self.assertEqual(wrapped.top_songs.filter(topsongrel__rank=1)[0].album,
                         "ギターと孤独と蒼い惑星")
        self.assertEqual(wrapped.top_songs.filter(topsongrel__rank=1)[0].artist_name,
                         "結束バンド")

        self.assertEqual(wrapped.top_songs.filter(topsongrel__rank=2)[0].name,
                         "Dreamer")
        self.assertEqual(wrapped.top_songs.filter(topsongrel__rank=2)[0].album,
                         "Everything All at Once")
        self.assertEqual(wrapped.top_songs.filter(topsongrel__rank=2)[0].artist_name,
                         "Sea in the Sky")

        self.assertEqual(wrapped.top_songs.filter(topsongrel__rank=3)[0].name,
                         "Juno")
        self.assertEqual(wrapped.top_songs.filter(topsongrel__rank=3)[0].album,
                         "Sonder")
        self.assertEqual(wrapped.top_songs.filter(topsongrel__rank=3)[0].artist_name,
                         "TesseracT")

        self.assertEqual(wrapped.top_songs.filter(topsongrel__rank=4)[0].name,
                         "Viscera")
        self.assertEqual(wrapped.top_songs.filter(topsongrel__rank=4)[0].album,
                         "Viscera")
        self.assertEqual(wrapped.top_songs.filter(topsongrel__rank=4)[0].artist_name,
                         "Veil Of Maya")

        self.assertEqual(wrapped.top_songs.filter(topsongrel__rank=5)[0].name,
                         "夜に駆ける")
        self.assertEqual(wrapped.top_songs.filter(topsongrel__rank=5)[0].album,
                         "THE BOOK")
        self.assertEqual(wrapped.top_songs.filter(topsongrel__rank=5)[0].artist_name,
                         "YOASOBI")
