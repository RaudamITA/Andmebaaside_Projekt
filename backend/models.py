from sqlalchemy.ext.automap import automap_base
from database import engine

Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# mapped classes are now created with names by default
# matching that of the table name.

# --------------------- Tables --------------------- #
Users = Base.classes.users
Hotels = Base.classes.hotels
Rooms = Base.classes.rooms
HotelAdmins = Base.classes.hotel_admins
HotelAmenities = Base.classes.hotel_amenities
RoomAmenities = Base.classes.room_amenities
HotelPictures = Base.classes.hotel_pictures
Bookings = Base.classes.bookings
