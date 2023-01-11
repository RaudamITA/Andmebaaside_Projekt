from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Rooms, RoomAmenities
from src.models.rooms import Room
from src.functions.token import validate_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
