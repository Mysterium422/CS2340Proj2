from home.spotify_api import SpotifyAPI
from home.spotify_api_pydantic import TopArtistsResponse, TopTracksResponse, RecommendationsResponse, ArtistObject, TrackObject
import json

class testSpotifyAPI(SpotifyAPI):
    def __init__(self, key=None):
        super().__init__(key)
    
    def submit_request(self, url):
        return None

    def get_top_artists_weekly(self, limit):
        f = open("test_resources/test_data/spotify_api/top_artist_weekly.json")
        data = json.load(f)

        return TopArtistsResponse.model_validate_json(data, strict=False)

    def get_top_artists_monthly(self, limit):
        f = open("test_resources/test_data/spotify_api/top_artist_monthly.json")
        data = json.load(f)

        return TopArtistsResponse.model_validate_json(data, strict=False)
    
    def get_top_artists_alltime(self, limit):
        f = open("test_resources/test_data/spotify_api/top_artist_alltime.json")
        data = json.load(f)

        return TopArtistsResponse.model_validate_json(data, strict=False)
    
    def get_top_tracks_weekly(self, limit):
        f = open("test_resources/test_data/spotify_api/top_tracks_weekly.json")
        data = json.load(f)

        return TopTracksResponse.model_validate_json(data, strict=False)
    
    def get_top_tracks_monthly(self, limit):
        f = open("test_resources/test_data/spotify_api/top_tracks_monthly.json")
        data = json.load(f)

        return TopTracksResponse.model_validate_json(data, strict=False)
    
    def get_top_tracks_alltime(self, limit):
        f = open("test_resources/test_data/spotify_api/top_tracks_alltime.json")
        data = json.load(f)

        return TopTracksResponse.model_validate_json(data, strict=False)
    
    def get_recently_played(self):
        f = open("test_resources/test_data/spotify_api/recently_played.json")
        data = json.load(f)

        return data
    
    def get_recommendations(self, limit, seed_tracks):
        f = open("test_resources/test_data/spotify_api/recommendations.json")
        data = json.load(f)

        return RecommendationsResponse.model_validate_json(data, strict=False)