"""
Mock API for Spotify API tests
"""

import json
from home.spotify_api import SpotifyAPI
from home.spotify_api_pydantic import TopArtistsResponse, TopTracksResponse, RecommendationsResponse


class TestSpotifyAPI(SpotifyAPI):
    """
    Mock API for Spotify API tests
    """
    def submit_request(self, _url):

        """
        Doesn't actually submit a request
        """
        return None

    def get_top_artists_weekly(self, _limit):
        """
        Get weekly top artists data from file
        """
        with open("test_resources/test_data/spotify_api/top_artist_weekly.json",
                  encoding="utf8") as f:
            data = json.load(f)
            return TopArtistsResponse.model_validate_json(data, strict=False)

    def get_top_artists_monthly(self, _limit):
        """
        Get monthly top artists data from file
        """
        with open("test_resources/test_data/spotify_api/top_artist_monthly.json",
                  encoding="utf8") as f:
            data = json.load(f)
            return TopArtistsResponse.model_validate_json(data, strict=False)

        return TopArtistsResponse.model_validate_json(data, strict=False)

    def get_top_artists_alltime(self, _limit):
        """
        Get all time top artists data from file
        """
        with open("test_resources/test_data/spotify_api/top_artist_alltime.json",
                  encoding="utf8") as f:
            data = json.load(f)
            return TopArtistsResponse.model_validate_json(data, strict=False)

    def get_top_tracks_weekly(self, _limit):
        """
        Get weekly top tracks data from file
        """
        with open("test_resources/test_data/spotify_api/top_tracks_weekly.json",
                  encoding="utf8") as f:
            data = json.load(f)
            return TopTracksResponse.model_validate_json(data, strict=False)

    def get_top_tracks_monthly(self, _limit):
        """
        Get monthly top tracks data from file
        """
        with open("test_resources/test_data/spotify_api/top_tracks_monthly.json",
                  encoding="utf8") as f:
            data = json.load(f)
            return TopTracksResponse.model_validate_json(data, strict=False)

    def get_top_tracks_alltime(self, _limit):
        """
        Get all time top tracks data from file
        """
        with open("test_resources/test_data/spotify_api/top_tracks_alltime.json",
                  encoding="utf8") as f:
            data = json.load(f)
            return TopTracksResponse.model_validate_json(data, strict=False)

    def get_recently_played(self):
        """
        Get recently played data from file
        """
        with open("test_resources/test_data/spotify_api/recently_played.json",
                  encoding="utf8") as f:
            data = json.load(f)
            return data

    def get_recommendations(self, _limit, _seed_tracks):
        """
        Get recommendations data from file
        """
        with open("test_resources/test_data/spotify_api/recommendations.json",
                  encoding="utf8") as f:
            data = json.load(f)
            return RecommendationsResponse.model_validate_json(data, strict=False)
