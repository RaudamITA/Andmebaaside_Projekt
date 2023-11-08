from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    status_code: int


class TokenData(BaseModel):
    username: str
