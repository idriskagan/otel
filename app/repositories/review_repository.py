from typing import List, Optional, Tuple
from app.extensions import db
from app.models.review import Review
from app.repositories.base_repository import BaseRepository


class ReviewRepository(BaseRepository[Review]):
    """OTEL-6.6: Review entity için veri erişim katmanı."""

    def __init__(self):
        super().__init__(Review)

    def get_by_hotel(self, hotel_id: int, page: int = 1, per_page: int = 10, sort_by: str = 'newest'):
        """Otele ait ana yorumları sayfalı döndürür."""
        query = (
            db.select(Review)
            .where(Review.hotel_id == hotel_id, Review.parent_id == None)
        )
        
        if sort_by == 'oldest':
            query = query.order_by(Review.created_at.asc())
        elif sort_by == 'highest':
            query = query.order_by(Review.rating.desc(), Review.created_at.desc())
        elif sort_by == 'lowest':
            query = query.order_by(Review.rating.asc(), Review.created_at.desc())
        else:
            query = query.order_by(Review.created_at.desc())
            
        return self.paginate(page=page, per_page=per_page, query=query)

    def get_average_rating(self, hotel_id: int) -> float:
        """Otelin ortalama puanını döndürür."""
        avg = db.session.execute(
            db.select(db.func.avg(Review.rating)).where(Review.hotel_id == hotel_id)
        ).scalar()
        return round(float(avg), 1) if avg else 0.0

    def get_user_review_for_hotel(self, user_id: int, hotel_id: int) -> Optional[Review]:
        """Kullanıcının bu otele daha önce yorum yapıp yapmadığını kontrol eder."""
        return db.session.execute(
            db.select(Review).where(
                Review.user_id == user_id,
                Review.hotel_id == hotel_id
            )
        ).scalar_one_or_none()
