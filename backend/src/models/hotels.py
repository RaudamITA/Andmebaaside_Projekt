from pydantic import BaseModel
from src.models.rooms import Room


class Owner(BaseModel):
    id: int | None = None
    first_name: str | None = None
    last_name: str | None = None

    class Config:
        orm_mode = True


class HotelAmenity(BaseModel):
    id: int | None = None
    hotel_id: int | None = None
    type: str | None = None
    amenity: str | None = None

    class Config:
        orm_mode = True


class HotelPicture(BaseModel):
    id: int | None = None
    hotel_id: int | None = None
    url: str | None = None

    class Config:
        orm_mode = True


class Hotel(BaseModel):
    id: int | None = None
    owners: list[Owner] | None = None
    name: str | None = None
    story_count: int | None = None
    stars: int | None = None
    address: str | None = None
    phone: str | None = None
    email: str | None = None
    website: str | None = None
    description: str | None = None
    amenities_in: list[HotelAmenity] | None = None
    amenities_out: list[HotelAmenity] | None = None
    pictures: list[HotelPicture] | None = None
    rooms: list[Room] | None = None

    class Config:
        orm_mode = True
