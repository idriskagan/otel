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
            self.review_repo.commit()
            return True, "Yorumunuz başarıyla eklendi.", review
        except Exception as e:
            self.review_repo.rollback()
            return False, f"Yorum eklenirken hata oluştu: {str(e)}", None

    def get_hotel_reviews(self, hotel_id: int, page: int = 1, per_page: int = 10, sort_by: str = 'newest') -> Dict[str, Any]:
        """Otele ait yorumları sayfalı şekilde ve ortalama puanla getirir."""
        pagination = self.review_repo.get_by_hotel(hotel_id, page=page, per_page=per_page, sort_by=sort_by)
        average_rating = self.review_repo.get_average_rating(hotel_id)
        
        return {
            'reviews': pagination.items,
            'total_pages': pagination.pages,
            'current_page': pagination.page,
            'total_reviews': pagination.total,
            'average_rating': average_rating
        }

    def edit_review(self, review_id: int, user_id: int, rating: int, comment: str) -> Tuple[bool, str]:
        """OTEL-31.1: Kullanıcının kendi yorumunu düzenlemesi."""
        review = self.review_repo.get_by_id(review_id)
        if not review:
            return False, "Yorum bulunamadı."
        if review.user_id != user_id:
            return False, "Bu yorumu düzenleme yetkiniz yok."
        if review.parent_id is not None:
            return False, "Yanıtlar düzenlenemez."
            
        try:
            review.rating = rating
            review.comment = comment
            review.is_edited = True
            self.review_repo.update(review)
            self.review_repo.commit()
            return True, "Yorumunuz güncellendi."
        except Exception as e:
            self.review_repo.rollback()
            return False, f"Güncelleme sırasında hata oluştu: {str(e)}"

    def delete_review(self, review_id: int, user_id: int) -> Tuple[bool, str]:
        """OTEL-31.1: Kullanıcının kendi yorumunu silmesi."""
        review = self.review_repo.get_by_id(review_id)
        if not review:
            return False, "Yorum bulunamadı."
        if review.user_id != user_id:
            return False, "Bu yorumu silme yetkiniz yok."
            
        try:
            self.review_repo.delete(review)
            self.review_repo.commit()
            return True, "Yorumunuz silindi."
        except Exception as e:
            self.review_repo.rollback()
            return False, f"Silme sırasında hata oluştu: {str(e)}"

    def add_reply(self, parent_id: int, user_id: int, comment: str) -> Tuple[bool, str]:
        """OTEL-31.2: Otel sahibinin yoruma yanıt vermesi."""
        parent_review = self.review_repo.get_by_id(parent_id)
        if not parent_review:
            return False, "Ana yorum bulunamadı."
        if parent_review.parent_id is not None:
            return False, "Bir yanıta yanıt verilemez."
            
        hotel = self.hotel_repo.get_by_id(parent_review.hotel_id)
        if not hotel or hotel.owner_id != user_id:
            return False, "Bu otele ait yorumlara yalnızca otel sahibi yanıt verebilir."
            
        try:
            reply = Review(
                user_id=user_id,
                hotel_id=hotel.id,
                rating=0,  # Yanıtlar oylama dışıdır, ancak db constraint yüzünden 0 veriyoruz.
                comment=comment,
                parent_id=parent_id
            )
            self.review_repo.create(reply)
            self.review_repo.commit()
            return True, "Yanıtınız eklendi."
        except Exception as e:
            self.review_repo.rollback()
            return False, f"Yanıt eklenirken hata oluştu: {str(e)}"

    def vote_helpful(self, review_id: int) -> Tuple[bool, str]:
        """OTEL-31.5: Yorumu faydalı bulma."""
        review = self.review_repo.get_by_id(review_id)
        if not review:
            return False, "Yorum bulunamadı."
        try:
            review.helpful_count += 1
            self.review_repo.update(review)
            self.review_repo.commit()
            return True, "Oyunuz kaydedildi."
        except Exception as e:
            self.review_repo.rollback()
            return False, f"Oy işlemi başarısız: {str(e)}"
