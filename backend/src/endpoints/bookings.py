from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import update
from sqlalchemy.orm import Session
from src.models.bookings import BookingIn, BookingOut
from src.functions.token import validate_token
from database.database import get_db
from database.models import Bookings, Users, Hotels, HotelAdmins


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# APIRouter creates path operations for user module
router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
    responses={404: {"description": "Not found"}},
)


# test Create booking
@router.post("/create")
async def create_booking(booking: BookingIn, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # Validate token
        token_data = validate_token(token)

        # Check if time is available
        if db.query(Bookings).filter(
            Bookings.hotel_id == booking.hotel_id,
            booking.check_in >= Bookings.check_in <= booking.check_out or booking.check_in <= Bookings.check_out >= booking.check_out
        ).first():
            return {"error": "Room is not available"}

        db.add(
            Bookings(
                user_id=booking.id,
                hotel_id=booking.hotel_id,
                room_id=booking.room_id,
                check_in=booking.check_in,
                check_out=booking.check_out,
                adult_count=booking.adult_count,
                child_count=booking.child_count,
                total_price=booking.total_price
            ))
        db.commit()

        return {"message": "Booking created"}
    except Exception as e:
        return {"error": "Error" + str(e)}


# test Get all hotel bookings
@router.get("/read/hotel/{hotel_id}/all", response_model=list[BookingOut])
async def get_all_hotel_bookings(hotel_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # Validate token
        token_data = validate_token(token)

        # Check if user is admin/owner and has read access
        token_owner = db.query(Users).filter(
            Users.username == token_data.username).first()
        relation_to_hotel = db.query(HotelAdmins).filter(
            HotelAdmins.user_id == token_owner.id).first()

        if relation_to_hotel.role != 'admin' or relation_to_hotel.role != 'owner':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

        if relation_to_hotel.read_permission == 0:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

        # Get all hotel bookings
        hotel_bookings = db.query(Bookings).filter(
            Bookings.hotel_id == hotel_id).all()

        return hotel_bookings
    except Exception as e:
        return {"error": "Error" + str(e)}


# test Get all user bookings
@router.get("/read/user/all", response_model=list[BookingOut])
async def get_all_user_bookings(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # Validate token
        token_data = validate_token(token)
        token_owner = db.query(Users).filter(
            Users.username == token_data.username).first()

        # Get all user bookings
        user_bookings = db.query(Bookings).filter(
            Bookings.user_id == token_owner.id).all()

        return user_bookings
    except Exception as e:
        return {"error": "Error" + str(e)}


# test Get all room bookings
@router.get("/read/room/{room_id}/all", response_model=list[BookingOut])
async def get_all_room_bookings(room_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # Validate token
        token_data = validate_token(token)

        # Check if user is admin/owner and has read access
        token_owner = db.query(Users).filter(
            Users.username == token_data.username).first()
        relation_to_hotel = db.query(HotelAdmins).filter(
            HotelAdmins.user_id == token_owner.id).first()

        if relation_to_hotel.role != 'admin' or relation_to_hotel.role != 'owner':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

        if relation_to_hotel.read_permission == 0:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

        # Get all room bookings
        room_bookings = db.query(Bookings).filter(
            Bookings.room_id == room_id).all()

        return room_bookings
    except Exception as e:
        return {"error": "Error" + str(e)}


# test Get booking by id
@router.get("/read/{booking_id}", response_model=BookingOut)
async def get_booking_by_id(booking_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # Validate token
        token_data = validate_token(token)
        token_owner = db.query(Users).filter(
            Users.username == token_data.username).first()

        # Check if user is either admin/owner or booking owner
        relation_to_hotel = db.query(HotelAdmins).filter(
            HotelAdmins.user_id == token_owner.id).first()
        booking_owner = db.query(Bookings).filter(
            Bookings.id == booking_id).first()

        if relation_to_hotel.role != 'admin' or relation_to_hotel.role != 'owner' or booking_owner.user_id != token_owner.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

        # Get booking by id
        booking = db.query(Bookings).filter(
            Bookings.id == booking_id).first()

        return booking
    except Exception as e:
        return {"error": "Error" + str(e)}


# test Get booking by hotel, room and user id
@router.get("/read/hotel/{hotel_id}/room/{room_id}/user/{user_id}", response_model=BookingOut)
async def get_room_by_hotel_room_user(hotel_id: int, room_id: int, user_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # Validate token
        token_data = validate_token(token)
        token_owner = db.query(Users).filter(
            Users.username == token_data.username).first()

        # Check if user is either admin/owner or booking owner
        relation_to_hotel = db.query(HotelAdmins).filter(
            HotelAdmins.user_id == token_owner.id).first()
        booking_owner = db.query(Bookings).filter(
            Bookings.user_id == user_id).first()

        if relation_to_hotel.role != 'admin' or relation_to_hotel.role != 'owner' or booking_owner.user_id != token_owner.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

        # Get booking by hotel, room and user id
        booking = db.query(Bookings).filter(
            Bookings.hotel_id == hotel_id and Bookings.room_id == room_id and Bookings.user_id == user_id).first()

        return booking
    except Exception as e:
        return {"error": "Error" + str(e)}


# todo Update booking
@router.put("/update/{booking_id}")
async def update_booking(booking_id: int, booking: BookingIn, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # Validate token
        token_data = validate_token(token)
        token_owner = db.query(Users).filter(
            Users.username == token_data.username).first()

        # Check if user is either admin/owner or booking owner
        relation_to_hotel = db.query(HotelAdmins).filter(
            HotelAdmins.user_id == token_owner.id).first()
        booking_owner = db.query(Bookings).filter(
            Bookings.id == booking_id).first()

        if relation_to_hotel.role != 'admin' or relation_to_hotel.role != 'owner' or booking_owner.user_id != token_owner.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

        # Update booking
        db.execute(update(booking).where(booking.id == booking_id).values(
            user_id=booking.user_id,
            hotel_id=booking.hotel_id,
            room_id=booking.room_id,
            check_in=booking.check_in,
            check_out=booking.check_out,
            adult_count=booking.adult_count,
            child_count=booking.child_count,
            total_price=booking.total_price,
        ))

        db.commit()

        return {"message": "Booking updated"}
    except Exception as e:
        return {"error": "Error" + str(e)}


# todo Delete booking
@router.delete("/delete/{booking_id}")
async def delete_booking(booking_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # Validate token
        token_data = validate_token(token)
        token_owner = db.query(Users).filter(
            Users.username == token_data.username).first()

        # Check if user is either admin/owner or booking owner
        relation_to_hotel = db.query(HotelAdmins).filter(
            HotelAdmins.user_id == token_owner.id).first()
        booking_owner = db.query(Bookings).filter(
            Bookings.id == booking_id).first()

        if relation_to_hotel.role != 'admin' or relation_to_hotel.role != 'owner' or booking_owner.user_id != token_owner.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

        # Delete booking
        db.query(Bookings).filter(Bookings.id == booking_id).delete()
        db.commit()

        return {"message": "Booking deleted"}
    except Exception as e:
        return {"error": "Error" + str(e)}
