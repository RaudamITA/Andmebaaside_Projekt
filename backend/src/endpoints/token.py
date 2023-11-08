from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import timedelta
from database.database import get_db
from database.models import Users
from src.models.token import Token
from src.functions.token import verify_password, create_access_token
from data import ACCESS_TOKEN_EXPIRE_MINUTES
from src.functions.log import log


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


router = APIRouter(
    prefix="/token",
    tags=["Token"],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # get user from db by username
    user = db.query(Users).filter(
        Users.username == form_data.username).first()
    # authenticate user
    if not user:
        log(user.username, 'Login for access token', '400', db=db)
        return {
            'message': 'Incorrect username or password',
            'status_code': status.HTTP_400_BAD_REQUEST,
            'headers': {'WWW-Authenticate': 'Bearer'}
        }
    if not verify_password(form_data.password, user.hashed_password):
        log(user.username, 'Login for access token', '400', db=db)
        return {
            'message': 'Incorrect username or password',
            'status_code': status.HTTP_400_BAD_REQUEST,
            'headers': {'WWW-Authenticate': 'Bearer'}
        }
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    await log(user.username, 'Login for access token', '200', db=db)

    return {"access_token": access_token, "token_type": "bearer", 'status_code': status.HTTP_200_OK}
