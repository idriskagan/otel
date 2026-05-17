from typing import Tuple, List, Dict, Any, Optional
from app.models.hotel import Hotel, HotelImage
from app.repositories.hotel_repository import HotelRepository
import os
from werkzeug.utils import secure_filename
from flask import current_app

class HotelService:
    """OTEL-13: Otel işlemleri için servis katmanı."""
    
    def __init__(self):
        self.hotel_repo = HotelRepository()
        
    def create_hotel(self, owner_id: int, data: Dict[str, Any]) -> Tuple[bool, str, Optional[Hotel]]:
        """Yeni bir otel kaydı oluşturur."""
        try:
            # Minimal validasyon
            if not data.get('name') or not data.get('city'):
                return False, "Otel adı ve şehir zorunludur.", None
                
            hotel = Hotel(
                owner_id=owner_id,
                name=data.get('name'),
                description=data.get('description'),
                city=data.get('city'),
                address=data.get('address'),
                star_rating=int(data.get('star_rating', 3)),
                phone=data.get('phone'),
                email=data.get('email'),
                is_approved=False # Yeni oteller onaya düşer
            )
            self.hotel_repo.create(hotel)
            return True, "Otel başarıyla eklendi, yönetici onayı bekleniyor.", hotel
        except Exception as e:
            return False, f"Otel eklenirken bir hata oluştu: {str(e)}", None

    def update_hotel(self, hotel_id: int, owner_id: int, data: Dict[str, Any]) -> Tuple[bool, str, Optional[Hotel]]:
        """Mevcut bir oteli günceller (sahiplik kontrolü ile)."""
        hotel = self.hotel_repo.get_by_id(hotel_id)
        if not hotel:
            return False, "Otel bulunamadı.", None
            
        if hotel.owner_id != owner_id:
            return False, "Bu oteli düzenleme yetkiniz yok.", None
            
        try:
            if 'name' in data: hotel.name = data['name']
            if 'description' in data: hotel.description = data['description']
            if 'city' in data: hotel.city = data['city']
            if 'address' in data: hotel.address = data['address']
            if 'star_rating' in data: hotel.star_rating = int(data['star_rating'])
            if 'phone' in data: hotel.phone = data['phone']
            if 'email' in data: hotel.email = data['email']
            
            self.hotel_repo.update(hotel)
            return True, "Otel başarıyla güncellendi.", hotel
        except Exception as e:
            return False, f"Güncelleme sırasında hata oluştu: {str(e)}", None

    def search_hotels(self, city: Optional[str] = None, min_stars: Optional[int] = None, is_approved: bool = True) -> List[Hotel]:
        """Otelleri filtreler."""
        # Şimdilik sadece city ve yıldız için basit arama, ileride repository içindeki search kullanılabilir
        query_args = {'is_approved': is_approved}
        if city:
            query_args['city'] = city
        # star_rating repository içinde filterlanacak, burada basit pass-through yapıyoruz.
        return self.hotel_repo.search(city=city, min_stars=min_stars, is_approved=is_approved)
        
    def approve_hotel(self, hotel_id: int) -> Tuple[bool, str]:
        """Oteli onaylar (Admin yetkisi gerektirir)."""
        hotel = self.hotel_repo.get_by_id(hotel_id)
        if not hotel:
            return False, "Otel bulunamadı."
            
        try:
            hotel.is_approved = True
            self.hotel_repo.update(hotel)
            return True, "Otel onaylandı."
        except Exception as e:
            return False, f"Onaylama sırasında hata oluştu: {str(e)}"
            
    def upload_images(self, hotel_id: int, owner_id: int, files: List[Any]) -> Tuple[bool, str]:
        """Otel fotoğraflarını yükler."""
        hotel = self.hotel_repo.get_by_id(hotel_id)
        if not hotel or hotel.owner_id != owner_id:
            return False, "Yetkisiz işlem veya otel bulunamadı."
            
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'app/static/uploads')
        os.makedirs(upload_folder, exist_ok=True)
        
        try:
            for file in files:
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    # İsim çakışmalarını önlemek için hotel_id ekle
                    save_name = f"hotel_{hotel_id}_{filename}"
                    save_path = os.path.join(upload_folder, save_name)
                    file.save(save_path)
                    
                    # Veritabanına kaydet
                    is_primary = hotel.images.count() == 0
                    new_image = HotelImage(
                        hotel_id=hotel_id,
                        image_path=f"uploads/{save_name}",
                        is_primary=is_primary
                    )
                    # Repository'e eklemek için: (Burada objeyi hotel.images'e append edip save edebiliriz)
                    self.hotel_repo.db.session.add(new_image)
            
            self.hotel_repo.db.session.commit()
            return True, "Fotoğraflar başarıyla yüklendi."
        except Exception as e:
            return False, f"Fotoğraf yüklenirken hata oluştu: {str(e)}"
