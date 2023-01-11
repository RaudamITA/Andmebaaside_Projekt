from pydantic import BaseModel


class RoomAmenity(BaseModel):
    id: int | None = None
    room_id: int | None = None
    amenity: str | None = None

    class Config:
        orm_mode = True


class Room(BaseModel):
    id: int | None = None
    hotel_id: int | None = None
    type: str | None = None
    price: int | None = None
    bed_count: int | None = None
    ext_bed_count: int | None = None
    room_number: int | None = None
    amenities: list[RoomAmenity] | None = None

    class Config:
        orm_mode = True
