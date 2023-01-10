from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import func, update
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
    username: str | None = None
    password: str | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    address: str | None = None

    class Config:
        orm_mode = True


# Hotel models

class Owner(BaseModel):
    id: int | None = None

    class Config:
        orm_mode = True


class HotelAmenity(BaseModel):
    id: int | None = None
    hotel_id: int | None = None
    type: str | None = None
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
    owner_id: list[Owner] | None = None
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


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
            username=user.username,
            hashed_password=get_password_hash(user.password),
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone,
            address=user.address
        ))

        db.commit()
        response = db.query(models.Users.username).filter(
            models.Users.id == user.id).first()
        return {"success": "User " + response[0] + " created successfully", "user_id": user.id}
    except Exception as e:
        return {"error": "Error: " + str(e)}


# Get user by id
@app.get("/users/read/id/{user_id}", response_model=User)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(models.Users).filter(
            models.Users.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user
    except Exception as e:
        return {"error": "Error: " + str(e)}


# Get user by token
@app.get("/users/read/me", response_model=User)
async def get_user_by_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        token_data = validate_token(token)
        user = db.query(models.Users).filter(
            models.Users.username == token_data.username).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user
    except Exception as e:
        return {"error": "Error: " + str(e)}


# Update user
@app.put("/users/update/{user_id}")
async def update_user_with_token(user_id: int, user: User, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        token_data = validate_token(token)
        token_owner_id = db.query(models.Users.id).filter(
            models.Users.username == token_data.username).first()[0]
        update_user = db.query(models.Users).filter(
            models.Users.id == user_id).first()
        print(user)

        # Update user
        if token_owner_id == user_id:
            db.execute(update(models.Users).where(models.Users.id == user_id).values(
                username=user.username if user.username else update_user.username,
                hashed_password=get_password_hash(
                    user.password) if user.password else update_user.hashed_password,
                email=user.email if user.email else update_user.email,
                first_name=user.first_name if user.first_name else update_user.first_name,
                last_name=user.last_name if user.last_name else update_user.last_name,
                phone=user.phone if user.phone else update_user.phone,
                address=user.address if user.address else update_user.address
            ))
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")

        db.commit()

        return {"success": "User " + user.username + " updated successfully"}

    except Exception as e:
        print(e)
        return {"error": "Error: " + str(e)}


# Delete user
@app.delete("/users/delete/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        # Validate token
        token_data = validate_token(token)

        # Get token owner id
        db_token_owner_id = db.query(models.Users.id).filter(
            models.Users.username == token_data.username).first()

        # Get users master id
        db_user_master_id = db.query(models.HotelAdmins.master_id).filter(
            models.HotelAdmins.user_id == user_id).first()

        if db_token_owner_id[0] == user_id or db_user_master_id == db_token_owner_id:
            db.query(models.Users).filter(models.Users.id == user_id).delete()
            db.commit()
            return {"success": "User deleted successfully"}
        else:
            return {"denied": "You are not authorized to delete this user"}

    except Exception as e:
        print(e)
        return {"error": "Error: " + str(e)}


# --------------------- Hotels --------------------- #

# Get all hotels
@app.get("/hotels/read/all", response_model=list[Hotel])
async def get_all_hotels(db: Session = Depends(get_db)):
    try:
        hotels = db.query(models.Hotels).all()

        for i in range(len(hotels)):
            hotels[i].owner_id = db.query(models.HotelAdmins.user_id).filter(
                models.HotelAdmins.hotel_id == hotels[i].id).all
            hotels[i].amenities_in = db.query(models.HotelAmenities).filter(
                models.HotelAmenities.hotel_id == hotels[i].id, models.HotelAmenities.type == "in").all()
            hotels[i].amenities_out = db.query(models.HotelAmenities).filter(
                models.HotelAmenities.hotel_id == hotels[i].id, models.HotelAmenities.type == "out").all()
            hotels[i].pictures = db.query(models.HotelPictures).filter(
                models.HotelPictures.hotel_id == hotels[i].id).all()
            hotels[i].rooms = db.query(models.Rooms).filter(
                models.Rooms.hotel_id == hotels[i].id).all()
            if hotels[i].rooms:
                for room in hotels[i].rooms:
                    room.amenities = db.query(models.RoomAmenities).filter(
                        models.RoomAmenities.room_id == room.id).all()

        return hotels
    except Exception as e:
        return {"error": "Error: " + str(e)}


# Get hotel by id
@app.get("/hotels/read/id/{hotel_id}", response_model=Hotel)
async def get_hotel_by_id(hotel_id: int, db: Session = Depends(get_db)):
    try:
        hotel = db.query(models.Hotels).filter(
            models.Hotels.id == hotel_id).first()

        hotel.owner_id = db.query(models.HotelAdmins.user_id).filter(
            models.HotelAdmins.hotel_id == hotel.id).all
        hotel.amenities_in = db.query(models.HotelAmenities).filter(
            models.HotelAmenities.hotel_id == hotel.id, models.HotelAmenities.type == "in").all()
        hotel.amenities_out = db.query(models.HotelAmenities).filter(
            models.HotelAmenities.hotel_id == hotel.id, models.HotelAmenities.type == "out").all()
        hotel.pictures = db.query(models.HotelPictures).filter(
            models.HotelPictures.hotel_id == hotel.id).all()
        hotel.rooms = db.query(models.Rooms).filter(
            models.Rooms.hotel_id == hotel.id).all()

        if hotel.rooms:
            for room in hotel.rooms:
                room.amenities = db.query(models.RoomAmenities).filter(
                    models.RoomAmenities.room_id == room.id).all()

        return hotel
    except Exception as e:
        return {"error": "Error: " + str(e)}


# test Get hotel by owner_id
@app.get("/hotels/read/owner_id/{owner_id}", response_model=list[Hotel])
async def get_hotel_by_owner_id(owner_id: int, db: Session = Depends(get_db)):
    try:
        hotel_ids = db.query(models.HotelAdmins.hotel_id).filter(
            models.HotelAdmins.user_id == owner_id).all()

        hotels = []

        for hotel_id in hotel_ids:
            hotel = db.query(models.Hotels).filter(
                models.Hotels.id == hotel_id).first()

            hotel.owner_id = db.query(models.HotelAdmins.user_id).filter(
                models.HotelAdmins.hotel_id == hotel.id).all
            hotel.amenities_in = db.query(models.HotelAmenities).filter(
                models.HotelAmenities.hotel_id == hotel.id, models.HotelAmenities.type == "in").all()
            hotel.amenities_out = db.query(models.HotelAmenities).filter(
                models.HotelAmenities.hotel_id == hotel.id, models.HotelAmenities.type == "out").all()
            hotel.pictures = db.query(models.HotelPictures).filter(
                models.HotelPictures.hotel_id == hotel.id).all()
            hotel.rooms = db.query(models.Rooms).filter(
                models.Rooms.hotel_id == hotel.id).all()

            if hotel.rooms:
                for room in hotel.rooms:
                    room.amenities = db.query(models.RoomAmenities).filter(
                        models.RoomAmenities.room_id == room.id).all()

            hotels.append(hotel)

        return hotels
    except Exception as e:
        return {"error": "Error: " + str(e)}


# test Get hotel by name
@app.get("/hotels/read/name/{name}", response_model=Hotel)
async def get_hotel_by_name(name: str, db: Session = Depends(get_db)):
    try:
        hotel = db.query(models.Hotels).filter(
            models.Hotels.name == name).first()

        hotel.owner_id = db.query(models.HotelAdmins.user_id).filter(
            models.HotelAdmins.hotel_id == hotel.id).all
        hotel.amenities_in = db.query(models.HotelAmenities).filter(
            models.HotelAmenities.hotel_id == hotel.id, models.HotelAmenities.type == "in").all()
        hotel.amenities_out = db.query(models.HotelAmenities).filter(
            models.HotelAmenities.hotel_id == hotel.id, models.HotelAmenities.type == "out").all()
        hotel.pictures = db.query(models.HotelPictures).filter(
            models.HotelPictures.hotel_id == hotel.id).all()
        hotel.rooms = db.query(models.Rooms).filter(
            models.Rooms.hotel_id == hotel.id).all()

        if hotel.rooms:
            for room in hotel.rooms:
                room.amenities = db.query(models.RoomAmenities).filter(
                    models.RoomAmenities.room_id == room.id).all()

        return hotel
    except Exception as e:
        return {"error": "Error: " + str(e)}


# Create hotel
@app.post("/hotels/create")
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
        hotel.id = (0 if db.query(func.max(models.Hotels.id)).scalar(
        ) == None else db.query(func.max(models.Users.id)).scalar(
        )) + 1

        # create hotel
        db.add(models.Hotels(
            id=hotel.id,
            name=hotel.name,
            story_count=hotel.story_count,
            stars=hotel.stars,
            address=hotel.address,
            phone=hotel.phone,
            email=hotel.email,
            website=hotel.website,
            description=hotel.description
        ))

        db.add(models.HotelAdmins(
            user_id=user.id,
            hotel_id=hotel.id,
            role="owner",
            create_permission=1,
            read_permission=1,
            update_permission=1,
            delete_permission=1
        ))

        if hotel.amenities_in:
            for amenity in hotel.amenities_in:
                db.add(models.HotelAmenities(
                    hotel_id=hotel.id,
                    type="in",
                    amenity=amenity
                ))

        if hotel.amenities_out:
            for amenity in hotel.amenities_out:
                db.add(models.HotelAmenities(
                    hotel_id=hotel.id,
                    type="out",
                    amenity=amenity
                ))

        if hotel.pictures:
            for picture in hotel.pictures:
                db.add(models.HotelPictures(
                    hotel_id=hotel.id,
                    picture=picture
                ))

        db.commit()

        if hotel.rooms:
            for room in hotel.rooms:
                room.id = (0 if db.query(func.max(models.Rooms.id)).scalar(
                ) == None else db.query(func.max(models.Rooms.id)).scalar(
                )) + 1
                db.add(models.Rooms(
                    id=room.id,
                    hotel_id=hotel.id,
                    room_number=room.room_number,
                    story=room.story,
                    price=room.price,
                    description=room.description
                ))
                if room.amenities:
                    for amenity in room.amenities:
                        db.add(models.RoomAmenities(
                            room_id=room.id,
                            amenity=amenity
                        ))
                db.commit()

        return {"success": "Hotel created"}
    except Exception as e:
        return {"error": "Error: " + str(e)}


# todo Update hotel


# test Delete hotel
@app.delete("/hotels/delete/{id}")
async def delete_hotel(id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        # Validate token
        token_data = validate_token(token)

        # Check if token owner is hotel owner
        if db.query(models.HotelAdmins).filter(
            models.HotelAdmins.user_id == token_data.user_id,
            models.HotelAdmins.hotel_id == id,
            models.HotelAdmins.role == "owner"
        ).first() == None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You do not have permission to delete this hotel",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Delete hotel
        db.query(models.Hotels).filter(
            models.Hotels.id == id).delete()
        db.commit()
    except Exception as e:
        return {"error": "Error: " + str(e)}


# test Create room
@app.post("/rooms/create")
async def create_room(room: Room, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        # Validate token
        token_data = validate_token(token)

        # Check if token owner is hotel owner
        if db.query(models.HotelAdmins).filter(
            models.HotelAdmins.user_id == token_data.user_id,
            models.HotelAdmins.hotel_id == room.hotel_id,
            models.HotelAdmins.role == "owner"
        ).first() == None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You do not have permission to create a room in this hotel",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create room
        room.id = (0 if db.query(func.max(models.Rooms.id)).scalar(
        ) == None else db.query(func.max(models.Rooms.id)).scalar(
        )) + 1
        db.add(models.Rooms(
            id=room.id,
            hotel_id=room.hotel_id,
            type=room.type,
            price=room.price,
            bed_count=room.bed_count,
            ext_bed_count=room.ext_bed_count,
            room_number=room.room_number,
        ))
        if room.amenities:
            for amenity in room.amenities:
                db.add(models.RoomAmenities(
                    room_id=room.id,
                    amenity=amenity
                ))
        db.commit()

        return {"success": f"Room {room.room_number} created"}
    except Exception as e:
        return {"error": "Error: " + str(e)}


# test Get room by hotel id and room number
@app.get("/rooms/get/{hotel_id}/{room_number}", response_model=Room)
async def get_room_by_hotel_id_and_room_number(hotel_id: int, room_number: int, db: Session = Depends(get_db)):
    try:
        room = db.query(models.Rooms).filter(
            models.Rooms.hotel_id == hotel_id,
            models.Rooms.room_number == room_number
        ).first()
        if room == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return room
    except Exception as e:
        return {"error": "Error: " + str(e)}


# todo Update room


# todo Delete room


# --------------------- Bookings --------------------- #

# todo Get all bookings


# todo Get booking by id


# todo Create booking


# todo Update booking


# todo Delete booking
