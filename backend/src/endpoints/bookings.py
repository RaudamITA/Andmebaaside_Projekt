from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from src.models.bookings import BookingIn, BookingOut
from src.functions.token import validate_token
from database.database import get_db
from database.models import Bookings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# APIRouter creates path operations for user module
router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
    responses={404: {"description": "Not found"}},
)
