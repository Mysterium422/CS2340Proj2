from spotify_api import SpotifyAPI
from spotify_api_pydantic import TopArtistsResponse, TopTracksResponse, RecommendationsResponse, ArtistObject, TrackObject
import json
from typing import override

class testSpotifyAPI(SpotifyAPI):
    def __init__(self, key=None):
        super().__init__(key)
    
    @override
    def submit_request(self, url):
        return None

    @override
    def get_top_artists_weekly(self, limit):
        f = open("test_resources/test_data/spotify_api/get_top_artists_weekly.json")
        data = json.load(f)

        return TopArtistsResponse.model_validate(data, strict=False)

    @override
    def get_top_artists_monthly(self, limit):
        f = open("test_resources/test_data/spotify_api/get_top_artists_monthly.json")
        data = json.load(f)

        return TopArtistsResponse.model_validate(data, strict=False)
    
    @override
    def get_top_artists_alltime(self, limit):
        f = open("test_resources/test_data/spotify_api/get_top_artists_alltime.json")
        data = json.load(f)

        return TopArtistsResponse.model_validate(data, strict=False)
    
    @override
    def get_top_tracks_weekly(self, limit):
        f = open("test_resources/test_data/spotify_api/get_top_tracks_weekly.json")
        data = json.load(f)

        return TopTracksResponse.model_validate(data, strict=False)
    
    @override
    def get_top_tracks_monthly(self, limit):
        f = open("test_resources/test_data/spotify_api/get_top_tracks_monthly.json")
        data = json.load(f)

        return TopTracksResponse.model_validate(data, strict=False)
    
    @override
    def get_top_tracks_alltime(self, limit):
        f = open("test_resources/test_data/spotify_api/get_top_tracks_alltime.json")
        data = json.load(f)

        return TopTracksResponse.model_validate(data, strict=False)
    
    @override
    def get_recently_played(self):
        f = open("test_resources/test_data/spotify_api/get_recently_played.json")
        data = json.load(f)

        return data
    
    @override
    def get_recommendations(self, limit, seed_tracks):
        f = open("test_resources/test_data/spotify_api/get_recommendations.json")
        data = json.load(f)

        return RecommendationsResponse.model_validate(data, strict=False)