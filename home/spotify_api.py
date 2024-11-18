import requests
from django.http import JsonResponse

from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class MyBaseModel(BaseModel):
    __slots__ = ()  # This limits Pydantic's internal properties in autocomplete

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True

class TopItemsResponse(MyBaseModel):
   href: str
   limit: int
   next: Optional[str]
   offset: int
   previous: Optional[str]
   total: int

class ExternalURLs(BaseModel):
   spotify: str

class ArtistFollowers(BaseModel):
   # href: null
   total: int

class ImageObject(BaseModel):
   url: str
   height: int
   width: int

class SimplifiedArtistObject(BaseModel):
   external_urls: ExternalURLs
   href: str
   id: str
   name: str
   type: str
   uri: str

class ArtistObject(SimplifiedArtistObject):
   followers: ArtistFollowers
   genres: List[str]
   images: List[ImageObject]
   popularity: int

class TopArtistsResponse(TopItemsResponse):
   items: List[ArtistObject]

class AlbumObject(BaseModel):
   album_type: str
   total_tracks: int
   available_markets: List[str]
   external_urls: ExternalURLs
   href: str
   id: str
   images: List[ImageObject]
   name: str
   release_date: str
   release_date_precision: str
   restrictions: Optional[Dict[str, str]] = Field(default=None)
   type: str
   uri: str
   artists: List[SimplifiedArtistObject]

class TrackObject(BaseModel):
   album: AlbumObject
   artists: List[SimplifiedArtistObject]
   available_markets: List[str]
   disc_number: int
   duration_ms: int
   explicit: bool
   external_ids: Dict[str, str]
   external_urls: ExternalURLs
   href: str
   id: str
   restrictions: Optional[Dict[str, str]] = Field(default=None)
   name: str
   popularity: int
   preview_url: str # Nullable
   track_number: int
   type: str
   uri: str
   is_local: bool

class TopTracksResponse(TopItemsResponse):
   items: List[TrackObject]

class SpotifyAPI:

  def __init__(self, key):
    self.key = key
    self.default_headers = {
        "Authorization": "Bearer " + self.key
    }

  def submit_request(self, url):
    response = requests.get(url, headers=self.default_headers)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

  def get_top_artists_weekly(self):
    url = "https://api.spotify.com/v1/me/top/artists?time_range=short_term"
    data = self.submit_request(url)
    return TopArtistsResponse.model_validate(data, strict=False)
  
  def get_top_artists_monthly(self):
    url = "https://api.spotify.com/v1/me/top/artists?time_range=medium_term"
    data = self.submit_request(url)
    return TopArtistsResponse.model_validate(data, strict=False)
  
  def get_top_artists_alltime(self):
    url = "https://api.spotify.com/v1/me/top/artists?time_range=long_term"
    data = self.submit_request(url)
    return TopArtistsResponse.model_validate(data, strict=False)
  
  def get_top_tracks_weekly(self):
    url = "https://api.spotify.com/v1/me/top/tracks?time_range=short_term"
    data = self.submit_request(url)
    return TopTracksResponse.model_validate(data, strict=False)
  
  def get_top_tracks_monthly(self):
    url = "https://api.spotify.com/v1/me/top/tracks?time_range=medium_term"
    data = self.submit_request(url)
    return TopTracksResponse.model_validate(data, strict=False)
  
  def get_top_tracks_alltime(self):
    url = "https://api.spotify.com/v1/me/top/tracks?time_range=long_term"
    data = self.submit_request(url)
    return TopTracksResponse.model_validate(data, strict=False)
  
  def get_recently_played(self):
    url = "https://api.spotify.com/v1/me/player/recently-played"
    return self.submit_request(url)
  


def main():
    def strip(s):
        return "".join(c for c in s if ord(c) < 0xff)

   
    p = SpotifyAPI("BQB-Zp2ETQ25le_FYD2JgSa6b4Aq8nx8hu1heNLIRcfTnx82KJXMIOVQPMfzjq2rR4U_PwPkFhugZLyFtPVz62XymKhrP7XUKRQGxUXB3TtgnOGak37WeVEHGH2TtHAeGoETvtb2meLmjwgNX4xGaPpVU5pa-q79EwOhrzmGoG-ceXQVeCn_JCpo2gozn9xnWN9owpunptpQlNeAocGuv41k6zM")
    out = p.get_top_artists_monthly()

    print(out.items[0].name)

   #  f = open("spotify_api_testlog5.txt", "w")
   #  f.write(strip(str(out)))

   #  f.write("\n")

   #  f.write(strip(str(out)))

   #  f.close()

   #  print(out.items[0].name)

if __name__ == "__main__":
    main()