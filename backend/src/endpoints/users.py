
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.models.users import UserOut, UserIn
from sqlalchemy import func, update
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Users, HotelAdmins
from src.functions.token import validate_token, get_password_hash


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
        return {"success": "User " + response[0] + " created successfully", "user_id": user.id}
    except Exception as e:
        return {"error": "Error: " + str(e)}


# Get user by id
@router.get("/read/id/{user_id}", response_model=UserOut)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(Users).filter(
            Users.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user
    except Exception as e:
        return {"error": "Error: " + str(e)}


# Get my Data
@router.get("/read/me", response_model=UserOut)
async def read_user_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        token_data = validate_token(token)
        user = db.query(Users).filter(
            Users.username == token_data.username).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user
    except Exception as e:
        return {"error": "Error: " + str(e)}


# Update user
@router.put("/update/{user_id}")
async def update_user_with_token(user_id: int, user: UserIn, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        token_data = validate_token(token)
        token_owner_id = db.query(Users.id).filter(
            Users.username == token_data.username).first()[0]
        update_user = db.query(Users).filter(
            Users.id == user_id).first()

        # Update user
        if token_owner_id == user_id:
            db.execute(update(Users).where(Users.id == user_id).values(
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

        return {"success": "User " + update_user.username + " updated successfully"}

    except Exception as e:
        print(e)
        return {"error": "Error: " + str(e)}


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
            return {"success": "User deleted successfully"}
        else:
            return {"denied": "You are not authorized to delete this user"}

    except Exception as e:
        print(e)
        return {"error": "Error: " + str(e)}
