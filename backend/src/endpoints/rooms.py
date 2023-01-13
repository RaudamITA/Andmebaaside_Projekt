from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Rooms, RoomAmenities, Users, HotelAdmins
from src.models.rooms import Room
from src.functions.token import validate_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# APIRouter creates path operations for user module
router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"],
    responses={404: {"description": "Not found"}},
)


# Get all hotel rooms
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
