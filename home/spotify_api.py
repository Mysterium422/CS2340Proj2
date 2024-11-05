import requests
from django.http import JsonResponse

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
        return {
            "error": response.status_code,
            "message": response.text
        }, response.status_code

  def get_top_artists_weekly(self):
    url = "https://api.spotify.com/v1/me/top/artists?time_range=short_term"
    return self.submit_request(url)
  
  def get_top_artists_monthly(self):
    url = "https://api.spotify.com/v1/me/top/artists?time_range=medium_term"
    return self.submit_request(url)
  
  def get_top_artists_alltime(self):
    url = "https://api.spotify.com/v1/me/top/artists?time_range=long_term"
    return self.submit_request(url)
  
  def get_top_tracks_weekly(self):
    url = "https://api.spotify.com/v1/me/top/tracks?time_range=short_term"
    return self.submit_request(url)
  
  def get_top_tracks_monthly(self):
    url = "https://api.spotify.com/v1/me/top/tracks?time_range=medium_term"
    return self.submit_request(url)
  
  def get_top_tracks_alltime(self):
    url = "https://api.spotify.com/v1/me/top/tracks?time_range=long_term"
    return self.submit_request(url)
  
  def get_recently_played(self):
    url = "https://api.spotify.com/v1/me/player/recently-played"
    return self.submit_request(url)
  


def main():
    def strip(s):
        return "".join(c for c in s if ord(c) < 0xff)

    p = SpotifyAPI("BQDgtRbH8q4yA1jwqrkyol1swhT1OMkDzHYDLGYxNqImOKYFIKri48Yh6xYsy3LPk-yZK_8anDgF4Ov0unAxUXStgPAC020V8PQLEBhnMPkBaFkdr1-Kv9N1yukQRbKMHwargTVJ285xJk9vB14hjfLOoKHpntDZPdniUod_IX8Satss6YBllsYEJeHT0uIXqrXIrmKsP_ssdVNmfaEkEG7WKQU")
    out = p.get_recently_played()

    f = open("spotify_api_testlog.txt", "w")
    f.write(strip(str(out)))

    f.write("\n")

    f.write(strip(str(out)))

    f.close()

if __name__ == "__main__":
    main()