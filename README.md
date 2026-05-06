Yapay Zeka Destekli Otel Kiralama Sistemi
# 🏨 StayFinder — Otel Rezervasyon Platformu

Türkiye genelinde otelleri arayın, karşılaştırın ve kolayca rezervasyon yapın.

## Teknolojiler
- **Backend:** Python 3.11+ / Flask
- **Veritabanı:** SQLAlchemy + SQLite
- **Auth:** Flask-Login
- **Frontend:** Jinja2 + Vanilla CSS/JS

## Kurulum

```bash
python -m venv venv
.\venv\Scripts\activate   # Windows
pip install -r requirements.txt
flask run
```

## Mimari
Katmanlı Mimari: Presentation → Service → Repository → Data
