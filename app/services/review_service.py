from typing import Tuple, Dict, Any, Optional
from app.models.review import Review
from app.repositories.review_repository import ReviewRepository
from app.repositories.hotel_repository import HotelRepository

class ReviewService:
    """OTEL-15: Yorum işlemleri için servis katmanı."""
    
    def __init__(self):
        self.review_repo = ReviewRepository()
        self.hotel_repo = HotelRepository()
        
    def add_review(self, user_id: int, hotel_id: int, rating: int, comment: str) -> Tuple[bool, str, Optional[Review]]:
        """Otele yeni yorum ekler. Aynı kullanıcı birden fazla yorum yapamaz."""
        
        hotel = self.hotel_repo.get_by_id(hotel_id)
        if not hotel:
            return False, "Otel bulunamadı.", None
            
        # Kullanıcının daha önceden yorum yapıp yapmadığı kontrol ediliyor
        existing_review = self.review_repo.get_user_review_for_hotel(user_id, hotel_id)
        if existing_review:
            return False, "Bu otele zaten daha önce yorum yaptınız.", None
            
        # Puan validasyonu
        if not (1 <= rating <= 5):
            return False, "Puan 1 ile 5 arasında olmalıdır.", None
            
        try:
            review = Review(
                user_id=user_id,
                hotel_id=hotel_id,
                rating=rating,
                comment=comment
            )
            self.review_repo.create(review)
            return True, "Yorumunuz başarıyla eklendi.", review
        except Exception as e:
            return False, f"Yorum eklenirken hata oluştu: {str(e)}", None

    def get_hotel_reviews(self, hotel_id: int, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """Otele ait yorumları sayfalı şekilde ve ortalama puanla getirir."""
        pagination = self.review_repo.get_by_hotel(hotel_id, page=page, per_page=per_page)
        average_rating = self.review_repo.get_average_rating(hotel_id)
        
        return {
            'reviews': pagination.items,
            'total_pages': pagination.pages,
            'current_page': pagination.page,
            'total_reviews': pagination.total,
            'average_rating': average_rating
        }
