from typing import List
from app.extensions import db
from app.models.amenity import Amenity
from app.repositories.base_repository import BaseRepository


class AmenityRepository(BaseRepository[Amenity]):
    """OTEL-6.4: Amenity entity için veri erişim katmanı."""

    def __init__(self):
        super().__init__(Amenity)

    def get_by_category(self, category: str) -> List[Amenity]:
        """Kategoriye göre özellikleri döndürür."""
        return db.session.execute(
            db.select(Amenity).where(Amenity.category == category).order_by(Amenity.name)
        ).scalars().all()

    def get_by_ids(self, ids: List[int]) -> List[Amenity]:
        """ID listesine göre özellikleri döndürür."""
        return db.session.execute(
            db.select(Amenity).where(Amenity.id.in_(ids))
        ).scalars().all()
