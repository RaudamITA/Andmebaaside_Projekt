from pydantic import BaseModel


class UserIn(BaseModel):
    id: int | None = None
    username: str | None = None
    password: str | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    address: str | None = None

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    id: int | None = None
    username: str | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    address: str | None = None

    class Config:
        orm_mode = True
