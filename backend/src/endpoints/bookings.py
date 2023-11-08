from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import func, update, delete, insert
from sqlalchemy.orm import Session
from src.models.bookings import BookingIn, BookingOut
from src.functions.token import validate_token
from database.database import get_db
from database.models import Bookings, Users, HotelAdmins, Rooms
from src.functions.log import log


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# APIRouter creates path operations for user module
router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
    responses={404: {"description": "Not found"}},
)


# Create booking
@router.post("/create")
async def create_booking(booking: BookingIn, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        token_data = validate_token(token)
        token_owner_id = db.query(Users.id).filter(
            Users.username == token_data.username).first()[0]

        db.execute(insert(Bookings).values(
            user_id=token_owner_id,
            hotel_id=booking.hotel_id,
            room_id=booking.room_id,
            check_in=booking.check_in,
            check_out=booking.check_out,
            adult_count=booking.adult_count,
            child_count=booking.child_count,
            total_price=booking.total_price,
            status=booking.status
        ))

        db.commit()

        await log(token_data.username, 'Create booking', '201', db=db)
        return {
            "message": "Booking created successfully",
            "status_code": status.HTTP_201_CREATED
        }
    except Exception as e:
        await log(token_data.username, 'Create booking', '400', db=db)
        return {
            "message": "Error: " + str(e),
            "status_code": status.HTTP_400_BAD_REQUEST
        }


# Get all hotel bookings
@router.get("/read/hotel/{hotel_id}/all", response_model=list[BookingOut])
async def get_all_hotel_bookings(hotel_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        token_data = validate_token(token)
        token_owner = db.query(Users).filter(
            Users.username == token_data.username).first()
        all_token_owners_hotel_ids = []
        for i in range(len(db.query(HotelAdmins).filter(HotelAdmins.user_id == token_owner.id).all())):
            all_token_owners_hotel_ids.append(
                db.query(HotelAdmins.hotel_id).filter(HotelAdmins.user_id == token_owner.id).all()[i][0])

        # Check that token owner is hotel admin or hotel owner
        if hotel_id not in all_token_owners_hotel_ids:
            return {'message': 'User is not room owner or admin', 'status_code': status.HTTP_401_UNAUTHORIZED}

        hotel_bookings = db.query(Bookings).filter(
            Bookings.hotel_id == hotel_id).all()

        return hotel_bookings

    except Exception as e:
        return {
            "message": "Error: " + str(e),
            "status_code": status.HTTP_400_BAD_REQUEST
        }


# Get all user bookings
@router.get("/read/user/all", response_model=list[BookingOut])
async def get_all_user_bookings(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        token_data = validate_token(token)
        token_owner_id = db.query(Users.id).filter(
            Users.username == token_data.username).first()[0]

        user_bookings = db.query(Bookings).filter(
            Bookings.user_id == token_owner_id).all()

        return user_bookings
    except Exception as e:
        return {
            "message": "Error: " + str(e),
            "status_code": status.HTTP_400_BAD_REQUEST
        }


# Get all room bookings
@router.get("/read/room/{room_id}/all", response_model=list[BookingOut])
async def get_all_room_bookings(room_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        token_data = validate_token(token)
        token_owner = db.query(Users).filter(
            Users.username == token_data.username).first()
        all_token_owners_hotel_ids = []
        for i in range(len(db.query(HotelAdmins).filter(HotelAdmins.user_id == token_owner.id).all())):
            all_token_owners_hotel_ids.append(
                db.query(HotelAdmins.hotel_id).filter(HotelAdmins.user_id == token_owner.id).all()[i][0])

        # rooms hotel id
        hotel_id = db.query(Rooms.hotel_id).filter(
            Rooms.id == room_id).first()[0]

        # Check that token owner is getting rooms for hotel they own
        if hotel_id not in all_token_owners_hotel_ids:
            return {'message': 'User is not room owner or admin', 'status_code': status.HTTP_401_UNAUTHORIZED}

        # Check if token owner is hotels owner or admin with update permission
        hotel_relation = db.query(HotelAdmins).filter(
            HotelAdmins.user_id == token_owner.id and HotelAdmins.hotel_id == hotel_id).first()
        if hotel_relation.update_permission == 0:
            return {'message': 'User does not have update permission', 'status_code': status.HTTP_401_UNAUTHORIZED}

        room_bookings = db.query(Bookings).filter(
            Bookings.room_id == room_id).all()

        return room_bookings

    except Exception as e:
        return {
            "message": "Error: " + str(e),
            "status_code": status.HTTP_400_BAD_REQUEST
        }


# Get booking by id
@router.get("/read/{booking_id}", response_model=BookingOut)
async def get_booking_by_id(booking_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        token_data = validate_token(token)
        token_owner = db.query(Users).filter(
            Users.username == token_data.username).first()
        all_token_owners_hotel_ids = []
        for i in range(len(db.query(HotelAdmins).filter(HotelAdmins.user_id == token_owner.id).all())):
            all_token_owners_hotel_ids.append(
                db.query(HotelAdmins.hotel_id).filter(HotelAdmins.user_id == token_owner.id).all()[i][0])

        booking = db.query(Bookings).filter(Bookings.id == booking_id).first()

        if booking.user_id == token_owner.id or booking.hotel_id in all_token_owners_hotel_ids:
            return booking

        else:
            print('here')
            return {'message': 'User is not booking owner or admin', 'status_code': status.HTTP_401_UNAUTHORIZED}

    except Exception as e:
        return {
            "message": "Error: " + str(e),
            "status_code": status.HTTP_400_BAD_REQUEST
        }


# Get booking by hotel, room and user id
@router.get("/read/hotel/{hotel_id}/room/{room_id}/user/{user_id}", response_model=BookingOut)
async def get_room_by_hotel_room_user(hotel_id: int, room_id: int, user_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        token_data = validate_token(token)
        token_owner = db.query(Users).filter(
            Users.username == token_data.username).first()
        all_token_owners_hotel_ids = []
        for i in range(len(db.query(HotelAdmins).filter(HotelAdmins.user_id == token_owner.id).all())):
            all_token_owners_hotel_ids.append(
                db.query(HotelAdmins.hotel_id).filter(HotelAdmins.user_id == token_owner.id).all()[i][0])

        if hotel_id not in all_token_owners_hotel_ids:
            return {'message': 'User is not hotel owner or admin', 'status_code': status.HTTP_401_UNAUTHORIZED}

        room = db.query(Rooms).filter(Rooms.id == room_id).first()

        if room.hotel_id != hotel_id:
            return {'message': 'Room is not in hotel', 'status_code': status.HTTP_400_BAD_REQUEST}

        booking = db.query(Bookings).filter(
            Bookings.hotel_id == hotel_id and Bookings.room_id == room_id and Bookings.user_id == user_id).first()

        return booking

    except Exception as e:
        return {
            "message": "Error: " + str(e),
            "status_code": status.HTTP_400_BAD_REQUEST
        }


# Update booking
@router.put("/update/{booking_id}")
async def update_booking(booking_id: int, booking: BookingIn, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        token_data = validate_token(token)
        token_owner = db.query(Users).filter(
            Users.username == token_data.username).first()
        all_token_owners_hotel_ids = []
        for i in range(len(db.query(HotelAdmins).filter(HotelAdmins.user_id == token_owner.id).all())):
            all_token_owners_hotel_ids.append(
                db.query(HotelAdmins.hotel_id).filter(HotelAdmins.user_id == token_owner.id).all()[i][0])

        # Check if token owner is hotels owner or admin with update permission
        hotel_relation = db.query(HotelAdmins).filter(
            HotelAdmins.user_id == token_owner.id and HotelAdmins.hotel_id == booking.hotel_id).first()
        if hotel_relation.update_permission == 0:
            await log(token_data.username, 'Update booking', '401', db=db)
            return {'message': 'User does not have update permission', 'status_code': status.HTTP_401_UNAUTHORIZED}

        # Check if booking exists
        booking_exists = db.query(Bookings).filter(
            Bookings.id == booking_id).first()
        if booking_exists is None:
            await log(token_data.username, 'Update booking', '400', db=db)
            return {'message': 'Booking does not exist', 'status_code': status.HTTP_400_BAD_REQUEST}

        # Update booking
        db.execute(
            update(Bookings).where(Bookings.id == booking_id).values(
                hotel_id=booking.hotel_id,
                room_id=booking.room_id,
                check_in=booking.check_in,
                check_out=booking.check_out,
                adult_count=booking.adult_count,
                child_count=booking.child_count,
                total_price=booking.total_price,
                status=booking.status
            )
        )
        db.commit()

        await log(token_data.username, 'Update booking', '200', db=db)
        return {'message': 'Booking updated', 'status_code': status.HTTP_200_OK}

    except Exception as e:
        await log(token_data.username, 'Update booking', '400', db=db)
        return {
            "message": "Error: " + str(e),
            "status_code": status.HTTP_400_BAD_REQUEST
        }


# Delete booking
@router.delete("/delete/{booking_id}")
async def delete_booking(booking_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        token_data = validate_token(token)
        token_owner = db.query(Users).filter(
            Users.username == token_data.username).first()
        all_token_owners_hotel_ids = []
        for i in range(len(db.query(HotelAdmins).filter(HotelAdmins.user_id == token_owner.id).all())):
            all_token_owners_hotel_ids.append(
                db.query(HotelAdmins.hotel_id).filter(HotelAdmins.user_id == token_owner.id).all()[i][0])

        booking = db.query(Bookings).filter(Bookings.id == booking_id).first()

        if booking.user_id == token_owner.id or booking.hotel_id in all_token_owners_hotel_ids:
            db.execute(delete(Bookings).where(Bookings.id == booking_id))
            db.commit()
            await log(token_data.username, 'Delete booking', '200', db=db)
            return {'message': 'Booking deleted', 'status_code': status.HTTP_200_OK}
        else:
            await log(token_data.username, 'Delete booking', '401', db=db)
            return {'message': 'User is not booking owner or admin', 'status_code': status.HTTP_401_UNAUTHORIZED}

    except Exception as e:
        await log(token_data.username, 'Delete booking', '400', db=db)
        return {
            "message": "Error: " + str(e),
            "status_code": status.HTTP_400_BAD_REQUEST
        }
