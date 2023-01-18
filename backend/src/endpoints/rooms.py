from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import func, update, delete, insert
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Rooms, RoomAmenities, Users, HotelAdmins, Bookings
from src.models.rooms import Room, AvailableRooms
from src.functions.token import validate_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# APIRouter creates path operations for user module
router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"],
    responses={404: {"description": "Not found"}},
)


# Create new room
@router.post("/create")
async def create_room(room: Room, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        token_data = validate_token(token)
        token_owner = db.query(Users).filter(
            Users.username == token_data.username
        ).first()
        all_token_owners_hotel_ids = []
        for i in range(len(db.query(HotelAdmins).filter(HotelAdmins.user_id == token_owner.id).all())):
            all_token_owners_hotel_ids.append(
                db.query(HotelAdmins.hotel_id).filter(HotelAdmins.user_id == token_owner.id).all()[i][0])

        # Check that token owner is creating room for hotel they own
        if room.hotel_id not in all_token_owners_hotel_ids:
            return {'message': 'User is not room owner or admin', 'status_code': status.HTTP_401_UNAUTHORIZED}

        # Check if token owner is hotels owner or admin with create permission
        hotel_relation = db.query(HotelAdmins).filter(
            HotelAdmins.user_id == token_owner.id and HotelAdmins.hotel_id == room.hotel_id).first()
        if hotel_relation.create_permission == 0:
            return {'message': 'User does not have create permission', 'status_code': status.HTTP_401_UNAUTHORIZED}

        # Check if room number already exists
        room_number = db.query(Rooms.room_number).filter(
            Rooms.room_number == room.room_number and Rooms.hotel_id == room.hotel_id).first()[0]
        if room_number == room.room_number:
            return {'message': 'Room number already exists', 'status_code': status.HTTP_400_BAD_REQUEST}

        # Create new room
        room.id = (0 if db.query(func.max(Rooms.id)).scalar() ==
                   None else db.query(func.max(Rooms.id)).scalar()) + 1

        db.add(Rooms(
            id=room.id,
            hotel_id=room.hotel_id,
            type=room.type,
            price=room.price,
            bed_count=room.bed_count,
            ext_bed_count=room.ext_bed_count,
            room_number=room.room_number))

        # db.commit()

        for amenity in room.amenities:
            print(amenity.amenity)
            db.add(RoomAmenities(
                room_id=room.id,
                amenity=amenity.amenity
            ))
            # db.commit()

        return {
            "message": "Room created successfully",
            "status_code": status.HTTP_201_CREATED
        }

    except Exception as e:
        return {
            "message": "Error: " + str(e),
            "status_code": status.HTTP_400_BAD_REQUEST
        }


# Get all hotel rooms
@router.get("/read/hotel/{hotel_id}", response_model=list[Room])
async def get_hotel_rooms(hotel_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        token_data = validate_token(token)
        token_owner = db.query(Users).filter(
            Users.username == token_data.username).first()
        all_token_owners_hotel_ids = []
        for i in range(len(db.query(HotelAdmins).filter(HotelAdmins.user_id == token_owner.id).all())):
            all_token_owners_hotel_ids.append(
                db.query(HotelAdmins.hotel_id).filter(HotelAdmins.user_id == token_owner.id).all()[i][0])

        # Check that token owner is getting rooms for hotel they own
        if hotel_id not in all_token_owners_hotel_ids:
            return {'message': 'User is not room owner or admin', 'status_code': status.HTTP_401_UNAUTHORIZED}

        # Check if token owner is hotels owner or admin with read permission
        hotel_relation = db.query(HotelAdmins).filter(
            HotelAdmins.user_id == token_owner.id and HotelAdmins.hotel_id == hotel_id).first()
        if hotel_relation.read_permission == 0:
            return {'message': 'User does not have read permission', 'status_code': status.HTTP_401_UNAUTHORIZED}

        # Get all rooms for hotel
        rooms = db.query(Rooms).filter(Rooms.hotel_id == hotel_id).all()
        for i in range(len(rooms)):
            rooms[i].amenities = db.query(RoomAmenities).filter(
                RoomAmenities.room_id == rooms[i].id).all()

        return rooms

    except Exception as e:
        return {
            "message": "Error: " + str(e),
            "status_code": status.HTTP_400_BAD_REQUEST
        }


# Update room
@router.put("/update/{room_id}")
async def update_room(room_id: int, room: Room, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        token_data = validate_token(token)
        token_owner = db.query(Users).filter(
            Users.username == token_data.username).first()
        all_token_owners_hotel_ids = []
        for i in range(len(db.query(HotelAdmins).filter(HotelAdmins.user_id == token_owner.id).all())):
            all_token_owners_hotel_ids.append(
                db.query(HotelAdmins.hotel_id).filter(HotelAdmins.user_id == token_owner.id).all()[i][0])

        # Check that token owner is getting rooms for hotel they own
        if room.hotel_id not in all_token_owners_hotel_ids:
            return {'message': 'User is not room owner or admin', 'status_code': status.HTTP_401_UNAUTHORIZED}

        # Check if token owner is hotels owner or admin with update permission
        hotel_relation = db.query(HotelAdmins).filter(
            HotelAdmins.user_id == token_owner.id and HotelAdmins.hotel_id == room.hotel_id).first()
        if hotel_relation.update_permission == 0:
            return {'message': 'User does not have update permission', 'status_code': status.HTTP_401_UNAUTHORIZED}

        # Update room
        db.execute(update(Rooms).where(Rooms.id == room_id).values(
            hotel_id=room.hotel_id,
            type=room.type,
            price=room.price,
            bed_count=room.bed_count,
            ext_bed_count=room.ext_bed_count,
            room_number=room.room_number
        ))

        # Update room amenities
        db.execute(delete(RoomAmenities).where(
            RoomAmenities.room_id == room_id))

        for amenity in room.amenities:
            db.execute(insert(RoomAmenities).values(
                room_id=room_id,
                amenity=amenity.amenity
            ))

        db.commit()

        return {
            "message": "Room updated successfully",
            "status_code": status.HTTP_201_CREATED
        }

    except Exception as e:
        return {
            "message": "Error: " + str(e),
            "status_code": status.HTTP_400_BAD_REQUEST
        }


# Delete room
@router.delete("/delete/{room_id}")
async def delete_room(room_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        token_data = validate_token(token)
        token_owner = db.query(Users).filter(
            Users.username == token_data.username).first()
        all_token_owners_hotel_ids = []
        for i in range(len(db.query(HotelAdmins).filter(HotelAdmins.user_id == token_owner.id).all())):
            all_token_owners_hotel_ids.append(
                db.query(HotelAdmins.hotel_id).filter(HotelAdmins.user_id == token_owner.id).all()[i][0])

        # Check that token owner is the owner of the room
        room = db.query(Rooms).filter(Rooms.id == room_id).first()
        if room.hotel_id not in all_token_owners_hotel_ids:
            return {'message': 'User is not room owner or admin', 'status_code': status.HTTP_401_UNAUTHORIZED}

        # Check if token owner is hotels owner or admin with delete permission
        hotel_relation = db.query(HotelAdmins).filter(
            HotelAdmins.user_id == token_owner.id and HotelAdmins.hotel_id == room.hotel_id).first()
        if hotel_relation.delete_permission == 0:
            return {'message': 'User does not have delete permission', 'status_code': status.HTTP_401_UNAUTHORIZED}

        # Delete room
        # Delete room amenities
        db.execute(delete(RoomAmenities).where(
            RoomAmenities.room_id == room_id))
        db.execute(delete(Rooms).where(Rooms.id == room_id))
        db.commit()

        return {
            "message": "Room deleted successfully",
            "status_code": status.HTTP_201_CREATED
        }

    except Exception as e:
        return {
            "message": "Error: " + str(e),
            "status_code": status.HTTP_400_BAD_REQUEST
        }


# FIXME: Get all available room types by hotel id and with check in and check out dates
@ router.post("/available/hotel/{hotel_id}")
async def get_available_rooms(hotel_id: int, times: AvailableRooms, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        validate_token(token)

        # return {
        #     "message": "Available rooms",
        #     "status_code": status.HTTP_200_OK,
        #     "available_rooms": available_rooms,
        #     "available_room_ids": available_room_ids
        # }

    except Exception as e:
        return {
            "message": "Error: " + str(e),
            "status_code": status.HTTP_400_BAD_REQUEST
        }
