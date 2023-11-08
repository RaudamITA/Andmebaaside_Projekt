
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from src.models.users import UserOut, UserIn
from sqlalchemy import func, update
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Users, HotelAdmins
from src.functions.token import validate_token, get_password_hash
from src.functions.log import log


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# APIRouter creates path operations for user module
router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)


# Create user
@router.post("/create")
async def create_user(user: UserIn, db: Session = Depends(get_db)):
    try:
        user.id = (0 if db.query(func.max(Users.id)).scalar(
        ) == None else db.query(func.max(Users.id)).scalar()) + 1
        db.add(Users(
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
        response = db.query(Users.username).filter(
            Users.id == user.id).first()
        
        await log(user.username, 'Create user', '201', db=db)
        return {
            "message": "User " + response[0] + " created successfully", "user_id": user.id,
            "status_code": status.HTTP_201_CREATED
        }
    except Exception as e:
        await log(user.username, 'Create user', '400', db=db)
        return {
            "message": "Error: " + str(e),
            "status_code": status.HTTP_400_BAD_REQUEST
        }


# Get user by id
@router.get("/read/id/{user_id}", response_model=UserOut)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(Users).filter(
            Users.id == user_id).first()

        if not user:
            return {
                "message": "User not found",
                "status_code": status.HTTP_404_NOT_FOUND
            }

        return user
    except Exception as e:
        return {
            "message": "Error: " + str(e),
            "status_code": status.HTTP_400_BAD_REQUEST
        }


# Get my Data
@router.get("/read/me", response_model=UserOut)
async def read_user_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        token_data = validate_token(token)
        user = db.query(Users).filter(
            Users.username == token_data.username).first()

        if not user:
            return {
                "message": "User not found",
                "status_code": status.HTTP_404_NOT_FOUND
            }

        return user
    except Exception as e:
        return {
            "message": "Error: " + str(e),
            "status_code": status.HTTP_400_BAD_REQUEST
        }


# Update user
@router.put("/update/{user_id}")
async def update_user_with_token(user_id: int, user: UserIn, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        token_data = validate_token(token)
        token_owner_id = db.query(Users.id).filter(
            Users.username == token_data.username).first()[0]
        original_user = db.query(Users).filter(
            Users.id == user_id).first()

        # Update user
        if token_owner_id == user_id:
            db.execute(update(Users).where(Users.id == user_id).values(
                username=user.username if user.username else original_user.username,
                hashed_password=get_password_hash(
                    user.password) if user.password else original_user.hashed_password,
                email=user.email if user.email else original_user.email,
                first_name=user.first_name if user.first_name else original_user.first_name,
                last_name=user.last_name if user.last_name else original_user.last_name,
                phone=user.phone if user.phone else original_user.phone,
                address=user.address if user.address else original_user.address
            ))
        else:
            return {
                "message": "Unauthorized",
                "status_code": status.HTTP_401_UNAUTHORIZED
            }

        db.commit()

        return {
            "message": "User " + original_user.username + " updated successfully",
            "status_code": status.HTTP_200_OK
        }

    except Exception as e:
        return {
            "message": "Error: " + str(e),
            "status_code": status.HTTP_400_BAD_REQUEST
        }


# Delete user
@router.delete("/delete/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        # Validate token
        token_data = validate_token(token)

        # Get token owner id
        db_token_owner_id = db.query(Users.id).filter(
            Users.username == token_data.username).first()

        # Get users master id
        db_user_master_id = db.query(HotelAdmins.master_id).filter(
            HotelAdmins.user_id == user_id).first()

        if db_token_owner_id[0] == user_id or db_user_master_id == db_token_owner_id:
            db.query(Users).filter(Users.id == user_id).delete()
            db.commit()
            return {
                "message": "User deleted successfully",
                "status_code": status.HTTP_200_OK
            }
        else:
            return {
                "message": "You are not authorized to delete this user",
                "status_code": status.HTTP_401_UNAUTHORIZED
            }

    except Exception as e:
        return {
            "message": "Error: " + str(e),
            "status_code": status.HTTP_400_BAD_REQUEST
        }
