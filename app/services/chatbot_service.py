from google import genai
from flask import current_app
from typing import Tuple
from app.repositories.hotel_repository import HotelRepository

class ChatbotService:
    """Yapay Zeka ve Chatbot işlemleri için servis katmanı (Yeni genai kütüphanesi)."""
    
    def __init__(self):
        self.hotel_repo = HotelRepository()

    def ask_hotel_assistant(self, hotel_id: int, user_message: str) -> Tuple[bool, str]:
        try:
            # 1. API Anahtarını al
            api_key = current_app.config.get('GEMINI_API_KEY')
            if not api_key:
                return False, "Sistem hatası: API anahtarı yapılandırılmamış."
                
            # 2. Yeni sisteme göre Client başlat
            client = genai.Client(api_key=api_key)

            # 3. Otel bilgilerini veritabanından getir
            hotel = self.hotel_repo.get_by_id(hotel_id)
            if not hotel:
                return False, "Otel bulunamadı."
            
            system_prompt = f"""
            Sen "{hotel.name}" isimli otelin yapay zeka destekli dijital asistanısın. Görevin otel müşterilerine yardımcı olmak.
            Çok kibar, profesyonel ve kısa (maksimum 2-3 cümle) cevaplar ver. 
            Sadece ama sadece aşağıdaki otel bilgilerini kullanarak cevap ver. Kendi başına fiyat, kural veya hizmet uydurma.
            Eğer sorunun cevabı aşağıdaki bilgilerde yoksa veya emin değilsen: "Bu konuda kesin bir bilgiye sahip değilim, detaylı bilgi için lütfen doğrudan otelle iletişime geçiniz." de.
            
            -- OTEL BİLGİLERİ --
            Otel Adı: {hotel.name}
            Şehir: {hotel.city}
            Yıldız: {hotel.star_rating} Yıldız
            Adres: {hotel.address}
            Genel Açıklama ve Kurallar: {hotel.description}
            İletişim: E-posta: {hotel.email or 'Belirtilmemiş'}, Telefon: {hotel.phone or 'Belirtilmemiş'}
            """

            full_prompt = f"{system_prompt}\n\nKULLANICI SORUSU: {user_message}\nCEVAP:"
            
            # 4. Yeni kütüphane ile modeli çağır (Listede gördüğünüz model adını buraya yazabilirsiniz)
            response = client.models.generate_content(
                model='gemini-flash-latest', 
                contents=full_prompt
            )
            
            # Markdown kalınlık işaretlerini temizle
            reply_text = response.text.replace('**', '').strip() 
            
            return True, reply_text

        except Exception as e:
            print(f"GEMINI API HATASI: {str(e)}")
            return False, "Şu an meşgulüm, lütfen daha sonra tekrar deneyin."