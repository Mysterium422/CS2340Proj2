"""
Pydantic models for Spotify API responses
"""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class MyBaseModel(BaseModel):
    """
    Base model for Pydantic models
    """
    __slots__ = ()  # This limits Pydantic's internal properties in autocomplete

    class Config:
        """
        Base model config
        """
        arbitrary_types_allowed = True
        use_enum_values = True


class TopItemsResponse(MyBaseModel):
    """
    Top items response model
    """
    href: str
    limit: int
    next: Optional[str]
    offset: int
    previous: Optional[str]
    total: int

class ExternalURLs(BaseModel):
    """
    Exernal URLs model
    """
    spotify: str

class ArtistFollowers(BaseModel):
    """
    Artist Followers model
    """
    # href: null
    total: int

class ImageObject(BaseModel):
    """
    Image object model
    """
    url: str
    height: int
    width: int

class SimplifiedArtistObject(BaseModel):
    """
    Simplified artist object model
    """
    external_urls: ExternalURLs
    href: str
    id: str
    name: str
    type: str
    uri: str

class ArtistObject(SimplifiedArtistObject):
    """
    Artist object model
    """
    followers: ArtistFollowers
    genres: List[str]
    images: List[ImageObject]
    popularity: int

class TopArtistsResponse(TopItemsResponse):
    """
    Top artists response model
    """
    items: List[ArtistObject]

class AlbumObject(BaseModel):
    """
    Album object model
    """
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
    """
    Track object model
    """
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
    track_number: int
    type: str
    uri: str
    is_local: bool

class TopTracksResponse(TopItemsResponse):
    """
    Top tracks model
    """
    items: List[TrackObject]

class RecommendationsResponse(MyBaseModel):
    """
    Recommendations response model
    """
    tracks: List[TrackObject]
