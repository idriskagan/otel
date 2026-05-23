from typing import List, Optional
from app.extensions import db
from app.models.favorite import Favorite
from app.models.hotel import Hotel
from app.repositories.base_repository import BaseRepository

class FavoriteRepository(BaseRepository[Favorite]):
    """OTEL-29.2: Favorite entity için veri erişim katmanı."""

    def __init__(self):
        super().__init__(Favorite)

    def get_by_user(self, user_id: int) -> List[Favorite]:
        """Kullanıcının favori otellerini döndürür."""
        return db.session.execute(
            db.select(Favorite).where(Favorite.user_id == user_id).order_by(Favorite.created_at.desc())
        ).scalars().all()

    def get_user_favorite_hotels(self, user_id: int) -> List[Hotel]:
        """Kullanıcının favoriye aldığı otel nesnelerini döndürür."""
        favorites = self.get_by_user(user_id)
        return [fav.hotel for fav in favorites]

    def get_favorite(self, user_id: int, hotel_id: int) -> Optional[Favorite]:
        """Belirli bir kullanıcı ve otel için favori kaydını döndürür."""
        return db.session.execute(
            db.select(Favorite).where(Favorite.user_id == user_id, Favorite.hotel_id == hotel_id)
        ).scalar_one_or_none()

    def is_favorited(self, user_id: int, hotel_id: int) -> bool:
        """Kullanıcının oteli favoriye alıp almadığını kontrol eder."""
        return self.get_favorite(user_id, hotel_id) is not None
