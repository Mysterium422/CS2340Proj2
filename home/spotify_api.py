import requests
from django.http import JsonResponse

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from models import Wrapped, Song, Artist, TopArtistRel, TopSongRel, TopWeeklyArtistRel, TopWeeklySongRel
from django.contrib.auth.models import User
from datetime import date

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

class RecommendationsResponse(MyBaseModel):
   tracks: List[TrackObject]

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

  def get_top_artists_weekly(self, limit):
    url = "https://api.spotify.com/v1/me/top/artists?time_range=short_term&limit=" + limit
    data = self.submit_request(url)
    return TopArtistsResponse.model_validate(data, strict=False)
  
  def get_top_artists_monthly(self, limit):
    url = "https://api.spotify.com/v1/me/top/artists?time_range=medium_term&limit=" + limit
    data = self.submit_request(url)
    return TopArtistsResponse.model_validate(data, strict=False)
  
  def get_top_artists_alltime(self, limit):
    url = "https://api.spotify.com/v1/me/top/artists?time_range=long_term&limit=" + limit
    data = self.submit_request(url)
    return TopArtistsResponse.model_validate(data, strict=False)
  
  def get_top_tracks_weekly(self, limit):
    url = "https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=" + limit
    data = self.submit_request(url)
    return TopTracksResponse.model_validate(data, strict=False)
  
  def get_top_tracks_monthly(self, limit):
    url = "https://api.spotify.com/v1/me/top/tracks?time_range=medium_term&limit=" + limit
    data = self.submit_request(url)
    return TopTracksResponse.model_validate(data, strict=False)
  
  def get_top_tracks_alltime(self, limit):
    url = "https://api.spotify.com/v1/me/top/tracks?time_range=long_term&limit=" + limit
    data = self.submit_request(url)
    return TopTracksResponse.model_validate(data, strict=False)
  
  def get_recently_played(self):
    url = "https://api.spotify.com/v1/me/player/recently-played"
    return self.submit_request(url)
  
  def get_recommendations(self, limit, seed_tracks):
     url = f"https://api.spotify.com/v1/recommendations?seed_tracks={seed_tracks}&limit={limit}"
     data = self.submit_request(url)
     return RecommendationsResponse.model_validate(data, strict=False)

def createArtist(artist: ArtistObject) -> Artist:
   artist_images = artist.images
   if len(artist_images > 0):
      return Artist.objects.create(name=artist.name, icon_href=artist.images[0].url)
   return Artist.objects.create(name=artist.name, icon_href="")

def createSong(song: TrackObject) -> Song:
   name = song.name
   song_artists = song.artists
   if (len(song_artists) > 0):
      artist_name = song_artists[0].name
   else:
      artist_name = ""
   
   album = song.album.name

   song_images = song.album.images

   if (len(song_images) > 0):
      song_image = song_images[0].url
   else:
      song_image = ""

   return Song.objects.create(name=name, artist_name=artist_name, album=album, icon_href=song_image)

def createWrapped(user: User, api: SpotifyAPI) -> Wrapped:
   wrapped = Wrapped.objects.create(user=user, date=date.today())

   lifetime_artists_result = api.get_top_artists_alltime(5).items

   for i in range(len(lifetime_artists_result)):
      lifetime_artist = lifetime_artists_result[i]
      artist = createArtist(lifetime_artist)
      rank = i+1
      TopArtistRel.objects.create(wrapped=wrapped, artist=artist, rank=rank)

   weekly_artists_result = api.get_top_artists_weekly(5).items

   for i in range(len(weekly_artists_result)):
      weekly_artist = weekly_artists_result[i]
      artist = createArtist(weekly_artist)
      rank = i+1
      TopWeeklyArtistRel.objects.create(wrapped=wrapped, artist=artist, rank=rank)
   
   weekly_songs_result = api.get_top_tracks_alltime(5).items
   song_seeds = []

   for i in range(len(weekly_songs_result)):
      weekly_song = weekly_songs_result[i]
      song = createSong(weekly_song)
      rank = i+1
      TopWeeklySongRel.objects.create(wrapped=wrapped, song=song, rank=rank)
      song_seeds.append(weekly_song.id)

   lifetime_songs_result = api.get_top_tracks_alltime(5).items

   for i in range(len(lifetime_songs_result)):
      lifetime_song = lifetime_songs_result[i]
      song = createSong(lifetime_song)
      rank = i+1
      TopSongRel.objects.create(wrapped=wrapped, song=song, rank=rank)
      if (len(song_seeds) < 5):
         song_seeds.append(lifetime_song.id)

   recommendations_result = api.get_recommendations(5, ",".join(song_seeds)).tracks
   recommended_songs = []

   for i in range(len(recommendations_result)):
      recommended_song = recommendations_result[i]
      song = createSong(recommended_song)
      recommended_songs.append(song)

   wrapped.recomended_songs.set(recommended_songs)

   return wrapped


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