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

class RecommendationsResponse(MyBaseModel):
   tracks: List[TrackObject]