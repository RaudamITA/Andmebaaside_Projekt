from pydantic import BaseModel

class log(BaseModel):
    id: int | None = None
    who: str | None = None
    what: str | None = None
    when: str | None = None
    status: str | None = None

    class Config:
        orm_mode = True