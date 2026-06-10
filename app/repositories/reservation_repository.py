from typing import List
from app.extensions import db
from app.models.reservation import Reservation
from app.repositories.base_repository import BaseRepository


class ReservationRepository(BaseRepository[Reservation]):
    """OTEL-6.5: Reservation entity için veri erişim katmanı."""

    def __init__(self):
        super().__init__(Reservation)

    def get_by_user(self, user_id: int) -> List[Reservation]:
        """Kullanıcıya ait tüm rezervasyonları döndürür."""
        return db.session.execute(
            db.select(Reservation)
            .where(Reservation.user_id == user_id)
            .order_by(Reservation.created_at.desc())
        ).scalars().all()

    def get_by_hotel(self, hotel_id: int) -> List[Reservation]:
        """Otele ait tüm rezervasyonları döndürür."""
        return db.session.execute(
            db.select(Reservation)
            .where(Reservation.hotel_id == hotel_id)
            .order_by(Reservation.check_in.asc())
        ).scalars().all()

    def count_all(self) -> int:
        return db.session.execute(
            db.select(db.func.count(Reservation.id))
        ).scalar()
