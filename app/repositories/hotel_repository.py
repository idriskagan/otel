from typing import List, Optional
from app.extensions import db
from app.models.hotel import Hotel
from app.repositories.base_repository import BaseRepository


class HotelRepository(BaseRepository[Hotel]):
    """OTEL-6.2: Hotel entity için veri erişim katmanı."""

    def __init__(self):
        super().__init__(Hotel)

    def get_approved(self, page: int = 1, per_page: int = 12):
        """Onaylanmış ve aktif otelleri sayfalı olarak döndürür."""
        query = (
            db.select(Hotel)
            .where(Hotel.is_approved == True, Hotel.is_active == True)
            .order_by(Hotel.created_at.desc())
        )
        return self.paginate(page=page, per_page=per_page, query=query)

    def get_by_owner(self, owner_id: int) -> List[Hotel]:
        """Otel sahibine ait tüm otelleri döndürür."""
        return db.session.execute(
            db.select(Hotel).where(Hotel.owner_id == owner_id)
        ).scalars().all()

    def search(self, city: str = None, stars: int = None,
               price_min: float = None, price_max: float = None,
               amenity_ids: List[int] = None,
               sort_by: str = 'newest',
               page: int = 1, per_page: int = 12):
        """Filtreli ve sıralı otel arama."""
        query = db.select(Hotel).where(
            Hotel.is_approved == True,
            Hotel.is_active == True
        )
        if city:
            query = query.where(Hotel.city.ilike(f'%{city}%'))
        if stars:
            query = query.where(Hotel.star_rating == stars)
        if price_min is not None:
            query = query.where(Hotel.price_min >= price_min)
        if price_max is not None:
            query = query.where(Hotel.price_max <= price_max)

        # Sıralama
        if sort_by == 'price_asc':
            query = query.order_by(Hotel.price_min.asc())
        elif sort_by == 'price_desc':
            query = query.order_by(Hotel.price_min.desc())
        elif sort_by == 'stars':
            query = query.order_by(Hotel.star_rating.desc())
        else:
            query = query.order_by(Hotel.created_at.desc())

        return self.paginate(page=page, per_page=per_page, query=query)

    def get_all_pending(self) -> List[Hotel]:
        """Admin için onay bekleyen otelleri döndürür."""
        return db.session.execute(
            db.select(Hotel).where(Hotel.is_approved == False)
        ).scalars().all()

    def get_distinct_cities(self) -> List[str]:
        """Onaylı otellerin bulunduğu şehirlerin listesini döndürür."""
        result = db.session.execute(
            db.select(Hotel.city).where(
                Hotel.is_approved == True, Hotel.is_active == True
            ).distinct().order_by(Hotel.city)
        ).scalars().all()
        return result

    def count_approved(self) -> int:
        return db.session.execute(
            db.select(db.func.count(Hotel.id)).where(Hotel.is_approved == True)
        ).scalar()
