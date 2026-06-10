from typing import Tuple, List
from app.extensions import db
from app.models.favorite import Favorite
from app.models.hotel import Hotel
from app.repositories.favorite_repository import FavoriteRepository
from app.repositories.hotel_repository import HotelRepository

class FavoriteService:
    """OTEL-29.3: Favori işlemleri için servis katmanı."""

    def __init__(self):
        self.fav_repo = FavoriteRepository()
        self.hotel_repo = HotelRepository()

    def toggle_favorite(self, user_id: int, hotel_id: int) -> Tuple[bool, str, bool]:
        """
        Kullanıcının oteli favoriye almasını veya favoriden çıkarmasını sağlar.
        Dönüş: (success, message, is_favorited)
        """
        hotel = self.hotel_repo.get_by_id(hotel_id)
        if not hotel:
            return False, "Otel bulunamadı.", False

        favorite = self.fav_repo.get_favorite(user_id, hotel_id)
        
        try:
            if favorite:
                # Zaten favorilerde, çıkar
                self.fav_repo.delete(favorite)
                self.fav_repo.commit()
                return True, "Otel favorilerden çıkarıldı.", False
            else:
                # Favorilerde yok, ekle
                new_favorite = Favorite(user_id=user_id, hotel_id=hotel_id)
                self.fav_repo.create(new_favorite)
                self.fav_repo.commit()
                return True, "Otel favorilere eklendi.", True
        except Exception as e:
            self.fav_repo.rollback()
            return False, f"İşlem sırasında hata oluştu: {str(e)}", False

    def get_user_favorites(self, user_id: int) -> List[Hotel]:
        """Kullanıcının favoriye aldığı otelleri döndürür."""
        return self.fav_repo.get_user_favorite_hotels(user_id)
