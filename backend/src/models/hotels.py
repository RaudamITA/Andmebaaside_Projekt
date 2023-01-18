from pydantic import BaseModel
from src.models.rooms import Room


class Owner(BaseModel):
    id: int | None = None
    first_name: str | None = None
    last_name: str | None = None

    class Config:
        orm_mode = True


class HotelAmenityBasic(BaseModel):
    amenity: str | None = None

    class Config:
        orm_mode = True


class HotelAmenityDetiled(BaseModel):
    id: int | None = None
    hotel_id: int | None = None
    type: str | None = None
    amenity: str | None = None

    class Config:
        orm_mode = True


class HotelPictureBasic(BaseModel):
    url: str | None = None

    class Config:
        orm_mode = True


class HotelPictureDetiled(BaseModel):
    id: int | None = None
    hotel_id: int | None = None
    url: str | None = None

    class Config:
        orm_mode = True


class HotelBasic(BaseModel):
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
    amenities_in: list[HotelAmenityBasic] | None = None
    amenities_out: list[HotelAmenityBasic] | None = None
    pictures: list[HotelPictureBasic] | None = None

    class Config:
        orm_mode = True


class HotelDetiled(BaseModel):
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
    amenities_in: list[HotelAmenityDetiled] | None = None
    amenities_out: list[HotelAmenityDetiled] | None = None
    pictures: list[HotelPictureDetiled] | None = None
    rooms: list[Room] | None = None

    class Config:
        orm_mode = True
