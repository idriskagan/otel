# OTEL-4.7: Tüm modelleri tek noktadan export et
from app.models.amenity import Amenity, hotel_amenities
from app.models.user import User
from app.models.hotel import Hotel, HotelImage
from app.models.room import RoomType
from app.models.reservation import Reservation
from app.models.review import Review

__all__ = [
    'User',
    'Hotel', 'HotelImage',
    'RoomType',
    'Amenity', 'hotel_amenities',
    'Reservation',
    'Review',
]
