from django.db import models
from django.contrib.auth.models import User

# Create your models here.

"""
Model for artist to be used in wrapped
name: name of the artist
icon_href: href to the icon of the artist
"""
class Artist(models.Model):
    name = models.CharField(max_length=128)
    icon_href = models.CharField(max_length=128)

"""
Model for song to be used in wrapped
name: name of the song
artist: foreign key to the artist of the song
album: name of the album the song is in
genre: genre of the song
icon_href: href to the icon of the song
"""
class Song(models.Model):
    name = models.CharField(max_length=128)
    artist_name = models.CharField(max_length=128)
    album = models.CharField(max_length=128)
    icon_href = models.CharField(max_length=128)

"""
Data for spotify wrapped
user: foreign key to the user that the wrapped is for
date: date of the wrapped
top_songs: many to many relationship to the top songs of the wrapped, relation includes a rank
top_artists: many to many relationship to the top artists of the wrapped, relation includes a rank
reccomended_songs: many to many relationship to the reccomended songs of the wrapped
"""
class Wrapped(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    top_songs = models.ManyToManyField(Song, through='TopSongRel', related_name='top_songs')
    top_weekly_songs = models.ManyToManyField(Song, through='TopWeeklySongRel', related_name='top_weekly_songs')
    top_artists = models.ManyToManyField(Artist, through='TopArtistRel', related_name='top_artists')
    top_weekly_artists = models.ManyToManyField(Artist, through='TopWeeklyArtistRel', related_name='top_weekly_artists')
    recomended_songs = models.ManyToManyField(Song, related_name='recomended_songs')

"""
Model for top song relation
wrapped: foreign key to the wrapped that the song is in
song: foreign key to the song
rank: rank of the song in the wrapped
"""
class TopSongRel(models.Model):
    wrapped = models.ForeignKey(Wrapped, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    rank = models.IntegerField()

"""
Model for top weekly song relation
wrapped: foreign key to the wrapped that the song is in
song: foreign key to the song
rank: rank of the song in the wrapped
"""
class TopWeeklySongRel(models.Model):
    wrapped = models.ForeignKey(Wrapped, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    rank = models.IntegerField()


"""
Model for top artist relation
wrapped: foreign key to the wrapped that the artist is in
song: foreign key to the artist
rank: rank of the artist in the wrapped
"""
class TopArtistRel(models.Model):
    wrapped = models.ForeignKey(Wrapped, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    rank = models.IntegerField()

"""
Model for top weekly artist relation
wrapped: foreign key to the wrapped that the artist is in
song: foreign key to the artist
rank: rank of the artist in the wrapped
"""
class TopWeeklyArtistRel(models.Model):
    wrapped = models.ForeignKey(Wrapped, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    rank = models.IntegerField()