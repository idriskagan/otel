from typing import Tuple, List, Optional
from datetime import date
from app.models.reservation import Reservation
from app.repositories.reservation_repository import ReservationRepository
from app.repositories.room_repository import RoomRepository
from app.repositories.hotel_repository import HotelRepository

class ReservationService:
    """OTEL-14: Rezervasyon işlemleri için servis katmanı."""
    
    def __init__(self):
        self.reservation_repo = ReservationRepository()
        self.room_repo = RoomRepository()
        self.hotel_repo = HotelRepository()
        
    def create_reservation(self, user_id: int, room_type_id: int, hotel_id: int, check_in: date, check_out: date, guests: int) -> Tuple[bool, str, Optional[Reservation]]:
        """Rezervasyon oluşturur. Çakışma kontrolü ve fiyat hesaplaması yapar."""
        
        if check_in >= check_out:
            return False, "Çıkış tarihi giriş tarihinden sonra olmalıdır.", None
            
        room = self.room_repo.get_by_id(room_type_id)
        if not room or room.hotel_id != hotel_id:
            return False, "Geçersiz oda tipi.", None
            
        if guests > room.capacity:
            return False, f"Bu oda tipi en fazla {room.capacity} kişi kapasitelidir.", None
            
        # Müsaitlik kontrolü
        is_available = self.room_repo.check_availability(room_type_id, check_in, check_out)
        if not is_available:
            return False, "Seçilen tarihlerde bu oda tipi için boş oda bulunmamaktadır.", None
            
        # Fiyat hesaplama
        nights = (check_out - check_in).days
        total_price = nights * room.price_per_night
        
        try:
            reservation = Reservation(
                user_id=user_id,
                hotel_id=hotel_id,
                room_type_id=room_type_id,
                check_in=check_in,
                check_out=check_out,
                guests=guests,
                total_price=total_price,
                status='pending'
            )
            self.reservation_repo.create(reservation)
            self.reservation_repo.commit()
            return True, "Rezervasyonunuz başarıyla oluşturuldu, onay bekleniyor.", reservation
        except Exception as e:
            self.reservation_repo.rollback()
            return False, f"Rezervasyon oluşturulurken bir hata oluştu: {str(e)}", None

    def cancel_reservation(self, reservation_id: int, user_id: int) -> Tuple[bool, str]:
        """Kullanıcının kendi rezervasyonunu iptal etmesini sağlar."""
        reservation = self.reservation_repo.get_by_id(reservation_id)
        
        if not reservation:
            return False, "Rezervasyon bulunamadı."
            
        if reservation.user_id != user_id:
            return False, "Bu işlemi yapmaya yetkiniz yok."
            
        if reservation.status == 'cancelled':
            return False, "Rezervasyon zaten iptal edilmiş."
            
        if reservation.check_in <= date.today():
            return False, "Geçmiş veya başlamış rezervasyonlar iptal edilemez."
            
        try:
            reservation.status = 'cancelled'
            self.reservation_repo.update(reservation)
            self.reservation_repo.commit()
            return True, "Rezervasyon başarıyla iptal edildi."
        except Exception as e:
            self.reservation_repo.rollback()
            return False, f"İptal sırasında hata oluştu: {str(e)}"
            
    def get_user_reservations(self, user_id: int) -> List[Reservation]:
        """Kullanıcıya ait tüm rezervasyonları getirir."""
        return self.reservation_repo.get_by_user(user_id)

    # --- İŞLETME SAHİBİ (OWNER) METODLARI ---

    def get_hotel_reservations(self, hotel_id: int, owner_id: int) -> List[Reservation]:
        """YENİ EKLENDİ: Otele ait rezervasyon taleplerini getirir (Sadece otel sahibi görebilir)."""
        hotel = self.hotel_repo.get_by_id(hotel_id)
        
        # Güvenlik Kontrolü: İşlemi yapan kişi otelin sahibi mi?
        if not hotel or hotel.owner_id != owner_id:
            return [] # Yetkisiz erişimse veya otel yoksa boş liste dön
            
        # Not: Eğer repository'nizde get_by_hotel fonksiyonu yoksa, 
        # ReservationRepository içine eklemeniz gerekecektir.
        return self.reservation_repo.get_by_hotel(hotel_id)

    def approve_reservation(self, reservation_id: int, user_id: int) -> Tuple[bool, str]:
        """İşletme sahibinin rezervasyonu onaylaması."""
        reservation = self.reservation_repo.get_by_id(reservation_id)
        
        if not reservation:
            return False, "Rezervasyon bulunamadı."
            
        # Güvenlik Kontrolü: İşlemi yapan kişi, otelin sahibi mi?
        hotel = self.hotel_repo.get_by_id(reservation.hotel_id)
        if not hotel or hotel.owner_id != user_id:
            return False, "Bu işlemi yapmaya yetkiniz yok."
            
        if reservation.status != 'pending':
            return False, "Sadece beklemedeki rezervasyonlar onaylanabilir."
            
        try:
            reservation.status = 'approved'
            self.reservation_repo.update(reservation)
            self.reservation_repo.commit()
            return True, "Rezervasyon başarıyla onaylandı."
        except Exception as e:
            self.reservation_repo.rollback()
            return False, f"Onaylama sırasında hata oluştu: {str(e)}"

    def reject_reservation(self, reservation_id: int, user_id: int) -> Tuple[bool, str]:
        """İşletme sahibinin rezervasyonu reddetmesi."""
        reservation = self.reservation_repo.get_by_id(reservation_id)
        
        if not reservation:
            return False, "Rezervasyon bulunamadı."
            
        # Güvenlik Kontrolü: İşlemi yapan kişi, otelin sahibi mi?
        hotel = self.hotel_repo.get_by_id(reservation.hotel_id)
        if not hotel or hotel.owner_id != user_id:
            return False, "Bu işlemi yapmaya yetkiniz yok."
            
        if reservation.status != 'pending':
            return False, "Sadece beklemedeki rezervasyonlar reddedilebilir."
            
        try:
            reservation.status = 'rejected'
            self.reservation_repo.update(reservation)
            self.reservation_repo.commit()
            return True, "Rezervasyon başarıyla reddedildi."
        except Exception as e:
            self.reservation_repo.rollback()
            return False, f"Reddetme sırasında hata oluştu: {str(e)}"