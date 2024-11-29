import requests
from django.http import JsonResponse

from typing import List, Dict, Optional
from home.models import Wrapped, Song, Artist, TopArtistRel, TopSongRel, TopWeeklyArtistRel, TopWeeklySongRel
from django.contrib.auth.models import User
from datetime import date
from home.spotify_api_pydantic import ArtistObject, TopArtistsResponse, TrackObject, TopTracksResponse, RecommendationsResponse

class SpotifyAPI:

  def __init__(self, key):
    self.key = key
    self.default_headers = {
        "Authorization": "Bearer " + str(self.key)
    }

  def submit_request(self, url):
    response = requests.get(url, headers=self.default_headers)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

  def get_top_artists_weekly(self, limit):
    limit = str(limit)
    url = "https://api.spotify.com/v1/me/top/artists?time_range=short_term&limit=" + limit
    data = self.submit_request(url)
    return TopArtistsResponse.model_validate(data, strict=False)
  
  def get_top_artists_monthly(self, limit):
    limit = str(limit)
    url = "https://api.spotify.com/v1/me/top/artists?time_range=medium_term&limit=" + limit
    data = self.submit_request(url)
    return TopArtistsResponse.model_validate(data, strict=False)
  
  def get_top_artists_alltime(self, limit):
    limit = str(limit)
    url = "https://api.spotify.com/v1/me/top/artists?time_range=long_term&limit=" + limit
    data = self.submit_request(url)
    return TopArtistsResponse.model_validate(data, strict=False)
  
  def get_top_tracks_weekly(self, limit):
    limit = str(limit)
    url = "https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=" + limit
    data = self.submit_request(url)
    return TopTracksResponse.model_validate(data, strict=False)
  
  def get_top_tracks_monthly(self, limit):
    limit = str(limit)
    url = "https://api.spotify.com/v1/me/top/tracks?time_range=medium_term&limit=" + limit
    data = self.submit_request(url)
    return TopTracksResponse.model_validate(data, strict=False)
  
  def get_top_tracks_alltime(self, limit):
    limit = str(limit)
    url = "https://api.spotify.com/v1/me/top/tracks?time_range=long_term&limit=" + limit
    data = self.submit_request(url)
    return TopTracksResponse.model_validate(data, strict=False)
  
  def get_recently_played(self):
    limit = str(limit)
    url = "https://api.spotify.com/v1/me/player/recently-played"
    return self.submit_request(url)
  
  def get_recommendations(self, limit, seed_tracks):
     limit = str(limit)
     url = f"https://api.spotify.com/v1/recommendations?seed_tracks={seed_tracks}&limit={limit}"
     data = self.submit_request(url)
     print(data)
     return RecommendationsResponse.model_validate(data, strict=False)

def createArtist(artist: ArtistObject) -> Artist:
   artist_images = artist.images
   if len(artist_images) > 0:
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
   
   weekly_songs_result = api.get_top_tracks_weekly(5).items
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
   import json 

   def strip(s):
       return "".join(c for c in s if ord(c) < 0xff)
   
   p = SpotifyAPI("BQDnAtI3U9fLwYq_HP1Y0T0pwjQKdcMtYR6hXykKDUBCU0_t4fC6Xy7yz_59Kwvs27hwjGnGIwyIp5H4CbypEkKlFDcd7-HfeDPnhPPsBT1SIPUqfwJ-R4LHflelp0gFtycaPuoK0vkj2zBDphUkMBSva8HlqHiLAfo1HI9yTEKJZGcI7wMhizNVSPZgV1X7k2TI1aDEtGqDDyOQwhIswtbF884")

   lifetime_songs_result = p.get_top_tracks_alltime('5').items

   seeds = []

   for song in (lifetime_songs_result[:5]):
      seeds.append(song.id)
 
   out = p.get_recommendations('5', ",".join(seeds))

   f = open("test_resources/recommendations.json", "w")
   json.dump(out.model_dump_json(), f)

   f.close()

if __name__ == "__main__":
    main()