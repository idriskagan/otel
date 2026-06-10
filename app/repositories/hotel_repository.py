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
               check_in: str = None, check_out: str = None,
               sort_by: str = 'newest',
               page: int = 1, per_page: int = 12):
        """Filtreli ve sıralı otel arama."""
        from app.models.amenity import Amenity
        from app.models.reservation import Reservation
        from app.models.room import RoomType
        from datetime import datetime
        
        query = db.select(Hotel).where(
            Hotel.is_approved == True,
            Hotel.is_active == True
        )
        if city:
            city_lower = city.lower()
            
            # 'i' harfi ile başlayan kelimelerde 'İ' dönüşümünü manuel yapıyoruz
            if city_lower.startswith('i'):
                city_tr_title = 'İ' + city_lower[1:]
            else:
                city_tr_title = city.title()

            # Veritabanında hem orijinal girilen metni, hem de baş harfi düzeltilmiş metni ara
            query = query.where(
                db.or_(
                    Hotel.city.ilike(f'%{city}%'),
                    Hotel.city.like(f'%{city_tr_title}%'),
                    Hotel.city.like(f'%{city_lower}%')
                )
            )
        if stars:
            query = query.where(Hotel.star_rating >= stars)
        if price_min is not None:
            query = query.where(Hotel.room_types.any(RoomType.price_per_night >= price_min))
        if price_max is not None:
            query = query.where(Hotel.room_types.any(RoomType.price_per_night <= price_max))

        if amenity_ids:
            for a_id in amenity_ids:
                query = query.where(Hotel.amenities.any(Amenity.id == a_id))

        if check_in and check_out:
            try:
                ci_date = datetime.strptime(check_in, '%Y-%m-%d').date()
                co_date = datetime.strptime(check_out, '%Y-%m-%d').date()
                
                conflict_res = (
                    db.select(Reservation.room_type_id, db.func.count(Reservation.id).label('booked'))
                    .where(
                        Reservation.status != 'cancelled',
                        Reservation.check_in < co_date,
                        Reservation.check_out > ci_date
                    )
                    .group_by(Reservation.room_type_id)
                    .subquery()
                )
                
                available_rooms_query = (
                    db.select(RoomType.hotel_id)
                    .outerjoin(conflict_res, RoomType.id == conflict_res.c.room_type_id)
                    .where(
                        RoomType.total_rooms > db.func.coalesce(conflict_res.c.booked, 0)
                    )
                )
                
                query = query.filter(Hotel.id.in_(available_rooms_query))
            except ValueError:
                pass

        # Sıralama
        if sort_by == 'price_asc':
            query = query.outerjoin(Hotel.room_types).order_by(RoomType.price_per_night.asc())
        elif sort_by == 'price_desc':
            query = query.outerjoin(Hotel.room_types).order_by(RoomType.price_per_night.desc())
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

    def count_all(self) -> int:
        """Toplam otel sayısını döndürür."""
        return db.session.execute(
            db.select(db.func.count(Hotel.id))
        ).scalar()
