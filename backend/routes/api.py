from fastapi import APIRouter
from src.endpoints import token, users, hotels, rooms, bookings

router = APIRouter()
router.include_router(token.router)
router.include_router(users.router)
router.include_router(hotels.router)
router.include_router(rooms.router)
router.include_router(bookings.router)
