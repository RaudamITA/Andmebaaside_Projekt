from pydantic import BaseModel


class BookingIn(BaseModel):
    user_id: int | None = None
    hotel_id: int | None = None
    room_id: int | None = None
    check_in: str | None = None
    check_out: str | None = None
    adult_count: int | None = None
    child_count: int | None = None
    total_price: float | None = None


class BookingOut(BaseModel):
    id: int | None = None
    user_id: int | None = None
    hotel_id: int | None = None
    room_id: int | None = None
    check_in: str | None = None
    check_out: str | None = None
    adult_count: int | None = None
    child_count: int | None = None
    total_price: float | None = None
