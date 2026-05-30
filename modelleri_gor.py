import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# .env dosyasının yerini kesin olarak belirtip yüklemesini garantiliyoruz
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Anahtarı kontrol et
api_key = os.environ.get('GEMINI_API_KEY')
if not api_key:
    print("HATA: .env dosyasından anahtar okunamadı! Lütfen dosya adının tam olarak .env olduğundan emin olun.")
    exit()

print("KULLANILABİLİR MODELLER LİSTESİ:")
print("-" * 30)

# Yeni kütüphane ile istemci (client) oluştur
client = genai.Client(api_key=api_key)

# Modelleri listele
for model in client.models.list():
    print(model.name)