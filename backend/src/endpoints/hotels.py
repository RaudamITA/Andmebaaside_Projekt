from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import func, update, delete
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Hotels, HotelAdmins, HotelAmenities, HotelPictures, Rooms, RoomAmenities, Users
from src.models.hotels import HotelBasic, HotelDetiled
from src.functions.token import validate_token
from src.functions.log import log


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# APIRouter creates path operations for user module
router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"],
    responses={404: {"description": "Not found"}},
)


# Create hotel
@router.post("/create")
async def create_hotel(hotel: HotelBasic, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        token_data = validate_token(token)

        # check if user has owner status
        user = db.query(Users).filter(
            Users.username == token_data.username).first()

        # take highest id and add 1
        hotel.id = (0 if db.query(func.max(Hotels.id)).scalar(
        ) == None else db.query(func.max(Hotels.id)).scalar(
        )) + 1

        # create hotel
        db.add(Hotels(
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

        db.add(HotelAdmins(
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
                db.add(HotelAmenities(
                    hotel_id=hotel.id,
                    type="in",
                    amenity=amenity.amenity
                ))

        if hotel.amenities_out:
            for amenity in hotel.amenities_out:
                db.add(HotelAmenities(
                    hotel_id=hotel.id,
                    type="out",
                    amenity=amenity.amenity
                ))

        if hotel.pictures:
            for picture in hotel.pictures:
                db.add(HotelPictures(
                    hotel_id=hotel.id,
                    url=picture.url
                ))

        db.commit()

        await log(user.username, 'Create hotel', '200', db=db)
        return {
            "message": "Hotel created successfully",
            "status_code": status.HTTP_200_OK
        }
    except Exception as e:
        await log(user.username, 'Create hotel', '400', db=db)
        return {
            "message": "Error: " + str(e),
            "status_code": status.HTTP_400_BAD_REQUEST
        }


# Get all hotels
@router.get("/read/all", response_model=list[HotelDetiled])
async def get_all_hotels(db: Session = Depends(get_db)):
    try:
        hotels = db.query(Hotels).all()

        for i in range(len(hotels)):
            hotel_owner_ids = []
            for j in range(len(db.query(HotelAdmins.user_id).filter(
                    HotelAdmins.hotel_id == hotels[i].id).all())):
                hotel_owner_ids.append(db.query(HotelAdmins.user_id).filter(
                    HotelAdmins.hotel_id == hotels[i].id).all()[j][0])

            hotels[i].owners = []
            for j in range(len(hotel_owner_ids)):
                hotels[i].owners.append({
                    "id": db.query(Users.id).filter(
                        Users.id == hotel_owner_ids[j]).first()[0],
                    "first_name": db.query(Users.first_name).filter(
                        Users.id == hotel_owner_ids[j]).first()[0],
                    "last_name": db.query(Users.last_name).filter(
                        Users.id == hotel_owner_ids[j]).first()[0]
                })

            hotels[i].amenities_in = db.query(HotelAmenities).filter(
                HotelAmenities.hotel_id == hotels[i].id, HotelAmenities.type == "in").all()
            hotels[i].amenities_out = db.query(HotelAmenities).filter(
                HotelAmenities.hotel_id == hotels[i].id, HotelAmenities.type == "out").all()
            hotels[i].pictures = db.query(HotelPictures).filter(
                HotelPictures.hotel_id == hotels[i].id).all()
            hotels[i].rooms = db.query(Rooms).filter(
                Rooms.hotel_id == hotels[i].id).all()
            if hotels[i].rooms:
                for room in hotels[i].rooms:
                    room.amenities = db.query(RoomAmenities).filter(
                        RoomAmenities.room_id == room.id).all()

        return hotels
    except Exception as e:
        return {
            "message": "Error: " + str(e),
            "status_code": status.HTTP_400_BAD_REQUEST
        }


# Get hotel by id
@router.get("/read/id/{hotel_id}", response_model=HotelDetiled)
async def get_hotel_by_id(hotel_id: int, db: Session = Depends(get_db)):
    try:
        hotel = db.query(Hotels).filter(
            Hotels.id == hotel_id).first()

        hotel_owner_ids = []
        for i in range(len(db.query(HotelAdmins.user_id).filter(
                HotelAdmins.hotel_id == hotel.id).all())):
            hotel_owner_ids.append(db.query(HotelAdmins.user_id).filter(
                HotelAdmins.hotel_id == hotel.id).all()[i][0])

        hotel.owners = []
        for i in range(len(hotel_owner_ids)):
            hotel.owners.append({
                "id": db.query(Users.id).filter(
                    Users.id == hotel_owner_ids[i]).first()[0],
                "first_name": db.query(Users.first_name).filter(
                    Users.id == hotel_owner_ids[i]).first()[0],
                "last_name": db.query(Users.last_name).filter(
                    Users.id == hotel_owner_ids[i]).first()[0]
            })

        hotel.amenities_in = db.query(HotelAmenities).filter(
            HotelAmenities.hotel_id == hotel.id, HotelAmenities.type == "in").all()
        hotel.amenities_out = db.query(HotelAmenities).filter(
            HotelAmenities.hotel_id == hotel.id, HotelAmenities.type == "out").all()
        hotel.pictures = db.query(HotelPictures).filter(
            HotelPictures.hotel_id == hotel.id).all()
        hotel.rooms = db.query(Rooms).filter(
            Rooms.hotel_id == hotel.id).all()

        if hotel.rooms:
            for room in hotel.rooms:
                room.amenities = db.query(RoomAmenities).filter(
                    RoomAmenities.room_id == room.id).all()

        return hotel
    except Exception as e:
        return {
            "message": "Error: " + str(e),
            "status_code": status.HTTP_400_BAD_REQUEST
        }


# Get hotel by name
@router.get("/read/name/{hotel_name}", response_model=HotelDetiled)
async def get_hotel_by_name(hotel_name: str, db: Session = Depends(get_db)):
    try:
        hotel = db.query(Hotels).filter(
            Hotels.name == hotel_name).first()

        hotel_owner_ids = []
        for i in range(len(db.query(HotelAdmins.user_id).filter(
                HotelAdmins.hotel_id == hotel.id).all())):
            hotel_owner_ids.append(db.query(HotelAdmins.user_id).filter(
                HotelAdmins.hotel_id == hotel.id).all()[i][0])

        hotel.owners = []
        for i in range(len(hotel_owner_ids)):
            hotel.owners.append({
                "id": db.query(Users.id).filter(
                    Users.id == hotel_owner_ids[i]).first()[0],
                "first_name": db.query(Users.first_name).filter(
                    Users.id == hotel_owner_ids[i]).first()[0],
                "last_name": db.query(Users.last_name).filter(
                    Users.id == hotel_owner_ids[i]).first()[0]
            })

        hotel.amenities_in = db.query(HotelAmenities).filter(
            HotelAmenities.hotel_id == hotel.id, HotelAmenities.type == "in").all()
        hotel.amenities_out = db.query(HotelAmenities).filter(
            HotelAmenities.hotel_id == hotel.id, HotelAmenities.type == "out").all()
        hotel.pictures = db.query(HotelPictures).filter(
            HotelPictures.hotel_id == hotel.id).all()
        hotel.rooms = db.query(Rooms).filter(
            Rooms.hotel_id == hotel.id).all()

        if hotel.rooms:
            for room in hotel.rooms:
                room.amenities = db.query(RoomAmenities).filter(
                    RoomAmenities.room_id == room.id).all()

        return hotel
    except Exception as e:
        return {
            "message": "Error: " + str(e),
            "status_code": status.HTTP_400_BAD_REQUEST
        }


# Get hotel by owner id
@router.get("/read/owner/{owner_id}", response_model=list[HotelDetiled])
async def get_hotel_by_owner_id(owner_id: int, db: Session = Depends(get_db)):
    try:
        hotel_ids = []
        for i in range(len(db.query(HotelAdmins.hotel_id).filter(
                HotelAdmins.user_id == owner_id).all())):
            hotel_ids.append(db.query(HotelAdmins.hotel_id).filter(
                HotelAdmins.user_id == owner_id).all()[i][0])

        hotels = []
        for i in range(len(hotel_ids)):
            hotels.append(db.query(Hotels).filter(
                Hotels.id == hotel_ids[i]).first())

        for i in range(len(hotels)):
            # Get hotel owners
            hotel_owner_ids = []
            for j in range(len(db.query(HotelAdmins.user_id).filter(
                    HotelAdmins.hotel_id == hotels[i].id).all())):
                hotel_owner_ids.append(db.query(HotelAdmins.user_id).filter(
                    HotelAdmins.hotel_id == hotels[i].id).all()[j][0])

            # Add hotel owners to hotel
            hotels[i].owners = []
            for j in range(len(hotel_owner_ids)):
                hotels[i].owners.append({
                    "id": db.query(Users.id).filter(
                        Users.id == hotel_owner_ids[j]).first()[0],
                    "first_name": db.query(Users.first_name).filter(
                        Users.id == hotel_owner_ids[j]).first()[0],
                    "last_name": db.query(Users.last_name).filter(
                        Users.id == hotel_owner_ids[j]).first()[0]
                })

            # Get hotel amenities
            hotels[i].amenities_in = db.query(HotelAmenities).filter(
                HotelAmenities.hotel_id == hotels[i].id, HotelAmenities.type == "in").all()
            hotels[i].amenities_out = db.query(HotelAmenities).filter(
                HotelAmenities.hotel_id == hotels[i].id, HotelAmenities.type == "out").all()

            # Get hotel pictures
            hotels[i].pictures = db.query(HotelPictures).filter(
                HotelPictures.hotel_id == hotels[i].id).all()

            # Get hotel rooms
            hotels[i].rooms = db.query(Rooms).filter(
                Rooms.hotel_id == hotels[i].id).all()

            # Get room amenities
            if hotels[i].rooms:
                for room in hotels[i].rooms:
                    room.amenities = db.query(RoomAmenities).filter(
                        RoomAmenities.room_id == room.id).all()

        return hotels

    except Exception as e:
        return {
            "message": "Error: " + str(e),
            "status_code": status.HTTP_400_BAD_REQUEST
        }


# Update hotel
@router.put("/update/{hotel_id}")
async def update_hotel(hotel_id: int, hotel: HotelBasic, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        token_data = validate_token(token)
        # Check if token owner is hotel owner
        hotel_owner_ids = []
        for i in range(len(db.query(HotelAdmins.user_id).filter(
                HotelAdmins.hotel_id == hotel_id).all())):
            hotel_owner_ids.append(db.query(HotelAdmins.user_id).filter(
                HotelAdmins.hotel_id == hotel_id).all()[i][0])

        token_owner_id = db.query(Users.id).filter(
            Users.username == token_data.username).first()[0]
        if token_owner_id not in hotel_owner_ids:
            await log(token_data.username, 'Update hotel', '401', db=db)
            return {
                "message": "You are not hotel owner",
                "status_code": status.HTTP_401_UNAUTHORIZED
            }

        original_hotel = db.query(Hotels).filter(
            Hotels.id == hotel_id).first()

        # Update hotel
        db.execute(update(Hotels).where(Hotels.id == hotel_id).values(
            name=hotel.name if hotel.name else original_hotel.name,
            story_count=hotel.story_count if hotel.story_count else original_hotel.story_count,
            stars=hotel.stars if hotel.stars else original_hotel.stars,
            address=hotel.address if hotel.address else original_hotel.address,
            phone=hotel.phone if hotel.phone else original_hotel.phone,
            email=hotel.email if hotel.email else original_hotel.email,
            website=hotel.website if hotel.website else original_hotel.website,
            description=hotel.description if hotel.description else original_hotel.description,
        ))

        # Update hotel amenities
        # Delete old hotel amenities
        db.execute(delete(HotelAmenities).where(
            HotelAmenities.hotel_id == hotel_id))

        # Add new hotel amenities
        for amenity in hotel.amenities_in:
            db.add(
                HotelAmenities(
                    hotel_id=hotel_id,
                    type="in",
                    amenity=amenity.amenity
                )
            )

        for amenity in hotel.amenities_out:
            db.add(
                HotelAmenities(
                    hotel_id=hotel_id,
                    type="out",
                    amenity=amenity.amenity
                )
            )

        # Update hotel pictures
        # Delete old hotel pictures
        db.execute(delete(HotelPictures).where(
            HotelPictures.hotel_id == hotel_id))

        # Add new hotel pictures
        for picture in hotel.pictures:
            db.add(
                HotelPictures(
                    hotel_id=hotel_id,
                    url=picture.url
                )
            )
        db.commit()

        await log(token_data.username, 'Create hotel', '200', db=db)
        return {
            "message": "Hotel updated successfully",
            "status_code": status.HTTP_200_OK
        }

    except Exception as e:
        await log(token_data.username, 'Create hotel', '400', db=db)
        return {
            "message": "Error: " + str(e),
            "status_code": status.HTTP_400_BAD_REQUEST
        }


# Delete hotel
@ router.delete("/delete/{hotel_id}")
async def delete_hotel(hotel_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        token_data = validate_token(token)
        # Get token owners id
        token_owner_id = db.query(Users.id).filter(
            Users.username == token_data.username).first()[0]

        # Check if token owner is hotel owner
        hotel_owner_ids = []
        for i in range(len(db.query(HotelAdmins.user_id).filter(
                HotelAdmins.hotel_id == hotel_id).all())):
            hotel_owner_ids.append(db.query(HotelAdmins.user_id).filter(
                HotelAdmins.hotel_id == hotel_id).all()[i][0])

        if token_owner_id not in hotel_owner_ids:
            await log(token_data.username, 'Delete hotel', '401', db=db)
            return {
                "message": "You are not hotel owner",
                "status_code": status.HTTP_401_UNAUTHORIZED
            }

        # Check if hotel exists
        hotel = db.query(Hotels).filter(Hotels.id == hotel_id).first()
        if not hotel:
            await log(token_data.username, 'Delete hotel', '401', db=db)
            return {
                "message": "Hotel does not exist",
                "status_code": status.HTTP_400_BAD_REQUEST
            }

        # Hotel deletion
        # Delete hotel owners
        db.query(HotelAdmins).filter(
            HotelAdmins.hotel_id == hotel_id).delete()

        # Delete hotel amenities
        db.query(HotelAmenities).filter(
            HotelAmenities.hotel_id == hotel_id).delete()

        # Delete hotel pictures
        db.query(HotelPictures).filter(
            HotelPictures.hotel_id == hotel_id).delete()

        # Delete hotel rooms
        hotel_room_ids = []
        for i in range(len(db.query(Rooms.id).filter(
                Rooms.hotel_id == hotel_id).all())):
            hotel_room_ids.append(db.query(Rooms.id).filter(
                Rooms.hotel_id == hotel_id).all()[i][0])

        # delete room amenities
        for i in range(len(hotel_room_ids)):
            db.query(RoomAmenities).filter(
                RoomAmenities.room_id == hotel_room_ids[i]).delete()

        # delete rooms
        db.query(Rooms).filter(
            Rooms.hotel_id == hotel_id).delete()

        # Delete hotel
        db.query(Hotels).filter(Hotels.id == hotel_id).delete()

        db.commit()

        await log(token_data.username, 'Delete hotel', '200', db=db)
        return {
            "message": "Hotel deleted successfully",
            "status_code": status.HTTP_200_OK
        }
    except Exception as e:
        await log(token_data.username, 'Delete hotel', '400', db=db)
        return {
            "message": "Error: " + str(e),
            "status_code": status.HTTP_400_BAD_REQUEST
        }
