"""
Module for spotify API wrapper
"""

from datetime import date
import requests

from django.contrib.auth.models import User

from home.models import Wrapped, Song, Artist, TopArtistRel
from home.models import TopSongRel, TopWeeklySongRel, TopWeeklyArtistRel
from home.spotify_api_pydantic import ArtistObject, TopArtistsResponse
from home.spotify_api_pydantic import TrackObject, TopTracksResponse, RecommendationsResponse

class SpotifyAPI:
    """
    Wrapper for Spotify API calls
    """

    def __init__(self, key):
        """
        Constructor for SpotifyAPI
        """
        self.key = key
        self.default_headers = {
            "Authorization": "Bearer " + str(self.key)
        }

    def submit_request(self, url):
        """
        Submit a request to the Spotify API
        url: full GET request URL
        """
        response = requests.get(url, headers=self.default_headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            return data

        raise Exception(f"Error {response.status_code}: {response.text}")

    def get_top_artists_weekly(self, limit):
        """
        Get top artists of the week for the user from the Spotify API
        """
        limit = str(limit)
        url = "https://api.spotify.com/v1/me/top/artists?time_range=short_term&limit=" + limit
        data = self.submit_request(url)
        return TopArtistsResponse.model_validate(data, strict=False)

    def get_top_artists_monthly(self, limit):
        """
        Get top artists of the month for the user from the Spotify API
        """
        limit = str(limit)
        url = "https://api.spotify.com/v1/me/top/artists?time_range=medium_term&limit=" + limit
        data = self.submit_request(url)
        return TopArtistsResponse.model_validate(data, strict=False)

    def get_top_artists_alltime(self, limit):
        """
        Get top artists of all time for the user from the Spotify API
        """
        limit = str(limit)
        url = "https://api.spotify.com/v1/me/top/artists?time_range=long_term&limit=" + limit
        data = self.submit_request(url)
        return TopArtistsResponse.model_validate(data, strict=False)

    def get_top_tracks_weekly(self, limit):
        """
        Get top tracks of the week for the user from the Spotify API
        """
        limit = str(limit)
        url = "https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=" + limit
        data = self.submit_request(url)
        return TopTracksResponse.model_validate(data, strict=False)

    def get_top_tracks_monthly(self, limit):
        """
        Get top tracks of the month for the user from the Spotify API
        """
        limit = str(limit)
        url = "https://api.spotify.com/v1/me/top/tracks?time_range=medium_term&limit=" + limit
        data = self.submit_request(url)
        return TopTracksResponse.model_validate(data, strict=False)

    def get_top_tracks_alltime(self, limit):
        """
        Get top tracks of all time for the user from the Spotify API
        """
        limit = str(limit)
        url = "https://api.spotify.com/v1/me/top/tracks?time_range=long_term&limit=" + limit
        data = self.submit_request(url)
        return TopTracksResponse.model_validate(data, strict=False)

    def get_recently_played(self):
        """
        Get recently played tracks for the user from the Spotify API
        """
        url = "https://api.spotify.com/v1/me/player/recently-played"
        return self.submit_request(url)

    def get_recommendations(self, limit, seed_tracks):
        """
        Get recommendations for the user from the Spotify API
        !!! Feature Depricated by Spotify !!!
        """
        limit = str(limit)
        url = f"https://api.spotify.com/v1/recommendations?seed_tracks={seed_tracks}&limit={limit}"
        data = self.submit_request(url)
        print(data)
        return RecommendationsResponse.model_validate(data, strict=False)

def create_artist(artist: ArtistObject) -> Artist:
    """
    Create an artist object from the Spotify API artist object
    """
    artist_images = artist.images
    if len(artist_images) > 0:
        return Artist.objects.create(name=artist.name, icon_href=artist.images[0].url)
    return Artist.objects.create(name=artist.name, icon_href="")

def create_song(song: TrackObject) -> Song:
    """
    Create a song object from the Spotify API track object
    """
    name = song.name
    song_artists = song.artists
    if len(song_artists) > 0:
        artist_name = song_artists[0].name
    else:
        artist_name = ""

    album = song.album.name

    song_images = song.album.images

    if len(song_images) > 0:
        song_image = song_images[0].url
    else:
        song_image = ""

    return Song.objects.create(name=name,
                               artist_name=artist_name,
                               album=album,
                               icon_href=song_image)

def create_wrapped(user: User, api: SpotifyAPI) -> Wrapped:
    """
    Create a wrapped object for the user
    """
    wrapped = Wrapped.objects.create(user=user, date=date.today())

    lifetime_artists_result = api.get_top_artists_alltime(5).items

    for i, lifetime_artist in enumerate(lifetime_artists_result):
        artist = create_artist(lifetime_artist)
        rank = i+1
        TopArtistRel.objects.create(wrapped=wrapped, artist=artist, rank=rank)

    weekly_artists_result = api.get_top_artists_weekly(5).items

    for i, weekly_artist in enumerate(weekly_artists_result):
        artist = create_artist(weekly_artist)
        rank = i+1
        TopWeeklyArtistRel.objects.create(wrapped=wrapped, artist=artist, rank=rank)

    weekly_songs_result = api.get_top_tracks_weekly(5).items
    song_seeds = []

    for i, weekly_song in enumerate(weekly_songs_result):
        song = create_song(weekly_song)
        rank = i+1
        TopWeeklySongRel.objects.create(wrapped=wrapped, song=song, rank=rank)
        song_seeds.append(weekly_song.id)

    lifetime_songs_result = api.get_top_tracks_alltime(5).items

    for i, lifetime_song in enumerate(lifetime_songs_result):
        song = create_song(lifetime_song)
        rank = i+1
        TopSongRel.objects.create(wrapped=wrapped, song=song, rank=rank)
        if len(song_seeds) < 5:
            song_seeds.append(lifetime_song.id)

   #  recommendations_result = api.get_recommendations(5, ",".join(song_seeds)).tracks
   #  recommended_songs = []

   #  for i, recommended_song in enumerate(recommendations_result):
      #   song = create_song(recommended_song)
      #   recommended_songs.append(song)

   #  wrapped.recomended_songs.set(recommended_songs)

    return wrapped
