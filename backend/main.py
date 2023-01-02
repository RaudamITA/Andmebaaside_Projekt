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

class User(BaseModel):
    id: int | None = None
    master_id: int | None = None
    role: str | None = None
    username: str | None = None
    password: str | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    address: str | None = None
    assigned_hotel_id: int | None = None
    create_permission: bool | None = None
    read_permission: bool | None = None
    update_permission: bool | None = None
    delete_permission: bool | None = None

    class Config:
        orm_mode = True


# Hotel models

class HotelAmenity(BaseModel):
    id: int | None = None
    hotel_id: int | None = None
    amenity: str | None = None

    class Config:
        orm_mode = True


class RoomAmenity(BaseModel):
    id: int | None = None
    room_id: int | None = None
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
    amenities: list[RoomAmenity] | None = None

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


# Create user
@app.post("/users/create")
async def create_user(user: User, db: Session = Depends(get_db)):
    try:
        user.id = (0 if db.query(func.max(models.Users.id)).scalar(
        ) == None else db.query(func.max(models.Users.id)).scalar()) + 1
        db.add(models.Users(
            id=user.id,
            master_id=user.master_id if user.master_id else None,
            role=user.role,
            username=user.username,
            hashed_password=get_password_hash(user.password),
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone,
            address=user.address,
            assigned_hotel_id=user.assigned_hotel_id,
            create_permission=int(user.create_permission),
            read_permission=int(user.read_permission),
            update_permission=int(user.update_permission),
            delete_permission=int(user.delete_permission)
        ))

        db.commit()

        return db.query(models.Users).filter(models.Users.id == user.id).first()
    except Exception as e:
        print(e)
        return {"message": "Error: " + str(e)}


# --------------------- Hotels --------------------- #

# Get all hotels
@ app.get("/hotels/all", response_model=list[Hotel])
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
@ app.get("/hotels/{hotel_id}", response_model=Hotel)
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


# Create hotel
@ app.post("/hotels/create")
async def create_hotel(hotel: Hotel, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        token_data = validate_token(token)

        # check if user has owner status
        user = db.query(models.Users).filter(
            models.Users.username == token_data.username).first()
        if user.role != "owner":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You do not have 'owner' status to create a hotel",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # take highest id and add 1
        hotel.id = db.query(func.max(models.Hotels.id)).scalar() + 1

        # create hotel
        db.add(models.Hotels(
            id=hotel.id,
            owner_id=user.id,
            name=hotel.name,
            story_count=hotel.story_count,
            stars=hotel.stars,
            address=hotel.address,
            phone=hotel.phone,
            email=hotel.email,
            website=hotel.website,
            description=hotel.description,
        ))

        # create amenities
        if hotel.amenities_in:
            for amenity in hotel.amenities_in:
                db.add(models.HotelAmenities(
                    hotel_id=hotel.id,
                    type="in",
                    name=amenity.amenity,
                ))
        if hotel.amenities_out:
            for amenity in hotel.amenities_out:
                db.add(models.HotelAmenities(
                    hotel_id=hotel.id,
                    type="out",
                    name=amenity.amenity,
                ))
        if hotel.pictures:
            for picture in hotel.pictures:
                db.add(models.HotelPictures(
                    hotel_id=hotel.id,
                    url=picture.url,
                ))

        db.commit()

        if hotel.rooms:
            for room in hotel.rooms:
                room.id = db.query(func.max(models.Rooms.id)).scalar() + 1
                db.add(models.Rooms(
                    room_id=room.id,
                    hotel_id=hotel.id,
                    type=room.name,
                    price=room.price,
                    bed_count=room.bed_count,
                    ext_bed_count=room.ext_bed_count,
                    room_number=room.room_number,
                ))

                if room.amenities:
                    for amenity in room.amenities:
                        db.add(models.RoomAmenities(
                            room_id=room.id,
                            name=amenity.amenity,
                        ))

                db.commit()

        return {"message": "Hotel created"}
    except Exception as e:
        return {"message": "Error: " + str(e)}
