from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import update
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


# test Create new room
@router.post("/create")
async def create_room(room: Room, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        token_data = validate_token(token)

        # Check if user is admin/owner and has create access
        token_owner = db.query(Users).filter(
            Users.username == token_data.username).first()
        relation_to_hotel = db.query(HotelAdmins).filter(
            HotelAdmins.user_id == token_owner.id).first()

        if token_owner.role != 'admin' or token_owner.role != 'owner':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

        if relation_to_hotel.create_permission == 0:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

        # Create new room
        new_room = Rooms(
            hotel_id=room.hotel_id,
            room_number=room.room_number,
            room_type=room.room_type,
            room_price=room.room_price,
            bed_count=room.bed_count,
            ext_bed_count=room.ext_bed_count
        )

        db.add(new_room)
        db.commit()

        # Create new room amenities
        for amenity in room.amenities:
            new_room_amenity = RoomAmenities(
                room_id=new_room.id,
                amenity=amenity
            )

            db.add(new_room_amenity)
            db.commit()

        return {"message": "Room created successfully"}

    except Exception as e:
        return {"error": "Error: " + str(e)}


# test Get all hotel rooms
@router.get("/read/hotel/{hotel_id}", response_model=Room)
async def get_hotel_rooms(hotel_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        token_data = validate_token(token)

        # Check if user is admin/owner and has read access
        token_owner = db.query(Users).filter(
            Users.username == token_data.username).first()
        relation_to_hotel = db.query(HotelAdmins).filter(
            HotelAdmins.user_id == token_owner.id).first()

        if token_owner.role != 'admin' or token_owner.role != 'owner':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

        if relation_to_hotel.read_permission == 0:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

        rooms = db.query(Rooms).filter(
            Rooms.hotel_id == hotel_id).all()

        for room in rooms:
            room.amenities = db.query(RoomAmenities).filter(
                RoomAmenities.room_id == room.id).all()

        return rooms

    except Exception as e:
        return {"error": "Error: " + str(e)}


# test Get room by hotel id and room number
@router.get("/read/hotel/{hotel_id}/room/{room_number}", response_model=Room)
async def get_room_by_number(hotel_id: int, room_number: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        token_data = validate_token(token)

        # Check if user is admin/owner and has read access
        token_owner = db.query(Users).filter(
            Users.username == token_data.username).first()
        relation_to_hotel = db.query(HotelAdmins).filter(
            HotelAdmins.user_id == token_owner.id).first()

        if token_owner.role != 'admin' or token_owner.role != 'owner':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

        if relation_to_hotel.read_permission == 0:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

        room = db.query(Rooms).filter(
            Rooms.hotel_id == hotel_id, Rooms.room_number == room_number).first()

        room.amenities = db.query(RoomAmenities).filter(
            RoomAmenities.room_id == room.id).all()

        return room

    except Exception as e:
        return {"error": "Error: " + str(e)}


# test Update room
@router.put("/update/{room_id}")
async def update_room(room_id: int, room: Room, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        token_data = validate_token(token)

        # Check if user is admin/owner and has update access
        token_owner = db.query(Users).filter(
            Users.username == token_data.username).first()
        relation_to_hotel = db.query(HotelAdmins).filter(
            HotelAdmins.user_id == token_owner.id).first()

        if token_owner.role != 'admin' or token_owner.role != 'owner':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

        if relation_to_hotel.update_permission == 0:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

        # Update room
        db.execute(update(Rooms).where(Rooms.id == room_id).values(
            hotel_id=room.hotel_id,
            room_number=room.room_number,
            room_type=room.room_type,
            room_price=room.room_price,
            bed_count=room.bed_count,
            ext_bed_count=room.ext_bed_count
        ))

        db.commit()

        # Delete old room amenities
        db.query(RoomAmenities).filter(
            RoomAmenities.room_id == room_id).delete()

        # Create new room amenities
        for amenity in room.amenities:
            new_room_amenity = RoomAmenities(
                room_id=room_id,
                amenity=amenity
            )

            db.add(new_room_amenity)
            db.commit()

        return {"message": "Room updated successfully"}

    except Exception as e:
        return {"error": "Error: " + str(e)}


# test Delete room
@router.delete("/delete/{room_id}")
async def delete_room(room_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        token_data = validate_token(token)

        # Check if user is admin/owner and has delete access
        token_owner = db.query(Users).filter(
            Users.username == token_data.username).first()
        relation_to_hotel = db.query(HotelAdmins).filter(
            HotelAdmins.user_id == token_owner.id).first()

        if token_owner.role != 'admin' or token_owner.role != 'owner':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

        if relation_to_hotel.delete_permission == 0:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

        # Delete room
        room = db.query(Rooms).filter(
            Rooms.id == room_id).first()

        db.delete(room)
        db.commit()

        return {"message": "Room deleted successfully"}

    except Exception as e:
        return {"error": "Error: " + str(e)}


# test Get all available room types by hotel id and with check in and check out dates
@router.get("/available/hotel/{hotel_id}")
async def get_available_rooms(hotel_id: int, times: AvailableRooms, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        validate_token(token)

        if times.check_in >= times.check_out:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Check in date must be before check out date")

        # Get all available rooms
        available_room_ids = db.query(Bookings.room_id).filter(
            Bookings.hotel_id == hotel_id,
            times.check_in <= Bookings.check_in >= times.check_out or times.check_in >= Bookings.check_out <= times.check_out
        ).all()

        available_rooms = []
        for id in available_room_ids:
            room_type = db.query(Rooms.type).filter(
                Rooms.id == id).first()
            if room_type not in available_rooms:
                available_rooms.append(room_type)

        return {"available_rooms": available_rooms, "available_room_ids": available_room_ids}

    except Exception as e:
        return {"error": "Error: " + str(e)}
