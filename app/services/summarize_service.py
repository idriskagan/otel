from google import genai
from flask import current_app
from typing import Tuple
from app.repositories.hotel_repository import HotelRepository

class SummarizeService:
    """Yapay Zeka ve Chatbot işlemleri için servis katmanı (Yeni genai kütüphanesi)."""
    
   
    def summarize_reviews(self, hotel_name: str, comments: list) -> tuple[bool, str]:
        """Otelin yorumlarını alıp Gemini ile özetler."""
        if not comments:
            return False, "Özetlenecek yeterli yorum bulunmuyor."

        try:
            # 1. API Anahtarını al ve Client başlat
            api_key = current_app.config.get('GEMINI_API_KEY')
            if not api_key:
                return False, "Sistem hatası: API anahtarı yapılandırılmamış."
                
            client = genai.Client(api_key=api_key)

            # 2. Yorumları tek bir metin haline getir 
            # (Çok uzun olmaması ve API sınırını aşmamak için en güncel 30 yorumu alıyoruz)
            reviews_text = "\n".join([f"- {comment}" for comment in comments[:30]])

            # 3. Sisteme nasıl özet çıkaracağını söyle
            system_prompt = f"""
            Sen uzman bir seyahat danışmanı ve otel değerlendirme asistanısın. 
            Aşağıda '{hotel_name}' oteli için müşteriler tarafından yapılmış yorumlar verilmiştir.
            Bu yorumları analiz et ve okuyucular için ÇOK KISA, vurucu ve net bir özet çıkar.
            
            KESİN KURALLAR:
            1. Her bölüm için MAKSİMUM 3 madde yazacaksın. Fazlası yasak.
            2. Maddeler çok kısa olacak (Maksimum 5-6 kelime). Uzun cümleler kurma.
            3. "Genel Karar" bölümü SADECE 1 CÜMLE olacak.
            
            KULLANILACAK FORMAT:
            🌟 **En Çok Beğenilenler:** 
            - (Kısa madde 1)
            - (Kısa madde 2)
            - (Kısa madde 3)
            
            ⚠️ **Dikkat Edilmesi Gerekenler:** 
            - (Kısa madde 1)
            - (Kısa madde 2)
            - (Kısa madde 3)
            
            💡 **Genel Karar:** (Sadece tek bir özet cümlesi)

            Sadece ve sadece aşağıdaki yorumlarda geçen bilgileri kullan. Yorumlarda geçmeyen hiçbir özelliği uydurma.
            """

            full_prompt = f"{system_prompt}\n\nMÜŞTERİ YORUMLARI:\n{reviews_text}"

            # 4. Modeli çağır (Daha önce listeden seçtiğimiz modeli kullanıyoruz)
            response = client.models.generate_content(
                model='gemini-flash-latest', 
                contents=full_prompt
            )
            
            return True, response.text

        except Exception as e:
            print(f"GEMINI ÖZET HATASI: {str(e)}")
            return False, "Yapay zeka şu an meşgul, lütfen daha sonra tekrar deneyin."