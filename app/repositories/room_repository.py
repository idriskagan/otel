from typing import List
from datetime import date
from app.extensions import db
from app.models.room import RoomType
from app.models.reservation import Reservation
from app.repositories.base_repository import BaseRepository


class RoomRepository(BaseRepository[RoomType]):
    """OTEL-6.3: RoomType entity için veri erişim katmanı."""

    def __init__(self):
        super().__init__(RoomType)

    def get_by_hotel(self, hotel_id: int) -> List[RoomType]:
        """Otele ait tüm oda tiplerini döndürür."""
        return db.session.execute(
            db.select(RoomType).where(RoomType.hotel_id == hotel_id)
        ).scalars().all()

    def check_availability(self, room_type_id: int, check_in: date, check_out: date) -> bool:
        """
        Belirtilen tarih aralığında oda müsaitliğini kontrol eder.
        Çakışan aktif rezervasyon varsa False döner.
        """
        room = db.session.get(RoomType, room_type_id)
        if not room:
            return False

        # Çakışan rezervasyonları say
        conflicting = db.session.execute(
            db.select(db.func.count(Reservation.id)).where(
                Reservation.room_type_id == room_type_id,
                Reservation.status.in_(['pending', 'confirmed']),
                Reservation.check_in < check_out,
                Reservation.check_out > check_in
            )
        ).scalar()

        return conflicting < room.total_rooms
