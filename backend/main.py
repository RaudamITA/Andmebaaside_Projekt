from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from database import SessionLocal
import data
import models


SECRET_KEY = data.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# --------------------- Models --------------------- #

# Token models
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


# User models


# Hotel models

class HotelAmenity(BaseModel):
    id: int | None = None
    hotel_id: int | None = None
    amenity: str | None = None

    class Config:
        orm_mode = True


class HotelPicture(BaseModel):
    id: int | None = None
    hotel_id: int | None = None
    url: str | None = None

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

    class Config:
        orm_mode = True


class Hotel(BaseModel):
    id: int | None = None
    owner_id: int | None = None
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


# --------------------- Functions --------------------- #

# Get database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create password hash
def get_password_hash(password):
    return pwd_context.hash(password)


# Verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Create access token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60*24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Validate token
def validate_token(token):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        return token_data
    except JWTError:
        raise credentials_exception


app = FastAPI()


# --------------------- Token --------------------- #

# Get token
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # get user from db by username
    user = db.query(models.Users).filter(
        models.Users.username == form_data.username).first()

    # authenticate user
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# --------------------- Users --------------------- #


# --------------------- Hotels --------------------- #

# Get all hotels
@app.get("/hotels/all", response_model=list[Hotel])
async def get_all_hotels(db: Session = Depends(get_db)):
    hotels = db.query(models.Hotels).all()

    for i in range(len(hotels)):
        hotels[i].amenities_in = db.query(models.HotelAmenities).filter(
            models.HotelAmenities.hotel_id == hotels[i].id, models.HotelAmenities.type == "in").all()
        hotels[i].amenities_out = db.query(models.HotelAmenities).filter(
            models.HotelAmenities.hotel_id == hotels[i].id, models.HotelAmenities.type == "out").all()
        hotels[i].pictures = db.query(models.HotelPictures).filter(
            models.HotelPictures.hotel_id == hotels[i].id).all()
        if hotels[i].rooms:
            hotels.room_count = len(hotels[i].rooms)

    return hotels


# Get hotel by id
@app.get("/hotels/{hotel_id}", response_model=Hotel)
async def get_hotel_by_id(hotel_id: int, db: Session = Depends(get_db)):
    hotel = db.query(models.Hotels).filter(
        models.Hotels.id == hotel_id).first()

    hotel.pictures = db.query(models.HotelPictures).filter(
        models.HotelPictures.hotel_id == hotel.id).all()
    hotel.rooms = db.query(models.Rooms).filter(
        models.Rooms.hotel_id == hotel.id).all()
    hotel.amenities_in = db.query(models.HotelAmenities).filter(
        models.HotelAmenities.hotel_id == hotel.id, models.HotelAmenities.type == "in").all()
    hotel.amenities_out = db.query(models.HotelAmenities).filter(
        models.HotelAmenities.hotel_id == hotel.id, models.HotelAmenities.type == "out").all()
    hotel.room_count = len(hotel.rooms)

    return hotel
