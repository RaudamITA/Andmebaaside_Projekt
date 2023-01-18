from pydantic import BaseModel


class BookingIn(BaseModel):
    hotel_id: int | None = None
    room_id: int | None = None
    check_in: str | None = None
    check_out: str | None = None
    adult_count: int | None = None
    child_count: int | None = None
    total_price: float | None = None
    status: str | None = None

    class Config:
        orm_mode = True


class BookingOut(BaseModel):
    id: int | None = None
    user_id: int | None = None
    hotel_id: int | None = None
    room_id: int | None = None
    check_in: str | None = None  # yyyy-mm-dd hh:mm:ss
    check_out: str | None = None  # yyyy-mm-dd hh:mm:ss
    adult_count: int | None = None
    child_count: int | None = None
    total_price: float | None = None
    status: str | None = None

    class Config:
        orm_mode = True
