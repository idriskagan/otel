# 🏨 Otel Projesi — Jira Task Board

> **Proje Kodu:** OTEL  
> **Git Branch Stratejisi:** `main` ← `develop` ← `feature/OTEL-XX-aciklama`  
> **Commit Format:** `[OTEL-XX] Açıklama`

---

## EPIC-1: Proje Altyapısı ve Konfigürasyon 🔵
**Tag:** `v0.1.0` | **Branch:** `feature/OTEL-epic-1-infrastructure`

### OTEL-1: Proje İskeleti Oluşturma
- `[ ]` **OTEL-1.1** Virtual environment oluştur (`python -m venv venv`)
- `[ ]` **OTEL-1.2** `requirements.txt` oluştur (Flask, SQLAlchemy, Migrate, Login, WTF, dotenv, Pillow)
- `[ ]` **OTEL-1.3** Bağımlılıkları yükle (`pip install -r requirements.txt`)
- `[ ]` **OTEL-1.4** `.gitignore` ve `.env` dosyalarını oluştur
> **Kabul Kriteri:** `pip freeze` ile tüm paketler yüklü görünmeli

### OTEL-2: Flask Application Factory
- `[ ]` **OTEL-2.1** `app/__init__.py` — create_app() factory fonksiyonu
- `[ ]` **OTEL-2.2** `app/config.py` — Dev/Prod/Test konfigürasyon sınıfları
- `[ ]` **OTEL-2.3** `app/extensions.py` — db, migrate, login_manager init
- `[ ]` **OTEL-2.4** `run.py` — Entry point
> **Kabul Kriteri:** `flask run` ile uygulama başlamalı, 200 OK dönmeli

### OTEL-3: Temel Dizin Yapısı
- `[ ]` **OTEL-3.1** `models/`, `repositories/`, `services/`, `routes/`, `forms/`, `utils/` klasörleri + `__init__.py`
- `[ ]` **OTEL-3.2** `templates/` ve `static/` klasör yapısı
- `[ ]` **OTEL-3.3** Minimal `base.html` template + `style.css` placeholder
- `[ ]` **OTEL-3.4** `README.md` oluştur
> **Kabul Kriteri:** Tüm klasörler mevcut, import hataları yok

🔖 **Commit:** `[OTEL-3] Proje altyapısı tamamlandı` → **Push & Tag v0.1.0**

---

## EPIC-2: Data Layer — Modeller ve Repository 🟢
**Tag:** `v0.2.0` | **Branch:** `feature/OTEL-epic-2-data-layer`

### OTEL-4: SQLAlchemy Modelleri
- `[ ]` **OTEL-4.1** `models/user.py` — User modeli (UserMixin, password hash/check)
- `[ ]` **OTEL-4.2** `models/hotel.py` — Hotel + HotelImage modelleri
- `[ ]` **OTEL-4.3** `models/room.py` — RoomType modeli
- `[ ]` **OTEL-4.4** `models/amenity.py` — Amenity + hotel_amenities M2M tablosu
- `[ ]` **OTEL-4.5** `models/reservation.py` — Reservation modeli
- `[ ]` **OTEL-4.6** `models/review.py` — Review modeli
- `[ ]` **OTEL-4.7** `models/__init__.py` — Tüm modelleri export et
> **Kabul Kriteri:** `flask db migrate` hatasız çalışmalı

### OTEL-5: Base Repository Pattern
- `[ ]` **OTEL-5.1** `repositories/base_repository.py` — Generic CRUD (get_by_id, get_all, create, update, delete, paginate)
> **Kabul Kriteri:** BaseRepository tüm modellerde kullanılabilir olmalı

### OTEL-6: Entity Repository'leri
- `[ ]` **OTEL-6.1** `repositories/user_repository.py` — get_by_email, get_by_username, get_by_role
- `[ ]` **OTEL-6.2** `repositories/hotel_repository.py` — search, filter_by_city, filter_by_stars, get_approved, get_by_owner
- `[ ]` **OTEL-6.3** `repositories/room_repository.py` — get_by_hotel, check_availability
- `[ ]` **OTEL-6.4** `repositories/amenity_repository.py` — get_all, get_by_category
- `[ ]` **OTEL-6.5** `repositories/reservation_repository.py` — get_by_user, get_by_hotel, get_conflicts
- `[ ]` **OTEL-6.6** `repositories/review_repository.py` — get_by_hotel, get_average_rating
> **Kabul Kriteri:** Her repository BaseRepository'den türemeli, özel sorgular çalışmalı

### OTEL-7: Migration ve Seed Data
- `[ ]` **OTEL-7.1** `flask db init` + `flask db migrate` + `flask db upgrade`
- `[ ]` **OTEL-7.2** `seed.py` — Admin kullanıcı, örnek amenity'ler, 3-5 örnek otel
- `[ ]` **OTEL-7.3** Seed script'i çalıştır ve doğrula
> **Kabul Kriteri:** DB oluşmalı, seed data yüklenmeli, ilişkiler doğru çalışmalı

🔖 **Commit:** `[OTEL-7] Data layer tamamlandı` → **Push & Tag v0.2.0**

---

## EPIC-3: Auth Sistemi — Service + Presentation 🟡
**Tag:** `v0.3.0` | **Branch:** `feature/OTEL-epic-3-auth`

### OTEL-8: Auth Service Layer
- `[ ]` **OTEL-8.1** `services/auth_service.py` — register_user(data): validasyon + hash + kayıt
- `[ ]` **OTEL-8.2** `services/auth_service.py` — login_user(email, password): doğrulama
- `[ ]` **OTEL-8.3** `services/auth_service.py` — Hata yönetimi (duplicate email, yanlış şifre)
> **Kabul Kriteri:** Service katmanı route'dan bağımsız test edilebilmeli

### OTEL-9: Auth Forms
- `[ ]` **OTEL-9.1** `forms/auth_forms.py` — LoginForm (email, password, CSRF)
- `[ ]` **OTEL-9.2** `forms/auth_forms.py` — RegisterForm (username, email, password, confirm, role)
> **Kabul Kriteri:** Validasyon kuralları (email format, min şifre uzunluğu) çalışmalı

### OTEL-10: Auth Routes (Presentation)
- `[ ]` **OTEL-10.1** `routes/auth.py` — Blueprint tanımla
- `[ ]` **OTEL-10.2** `GET/POST /login` — Giriş sayfası
- `[ ]` **OTEL-10.3** `GET/POST /register` — Kayıt sayfası (kullanıcı/otel sahibi seçimi)
- `[ ]` **OTEL-10.4** `GET /logout` — Çıkış
- `[ ]` **OTEL-10.5** Flask-Login user_loader callback
> **Kabul Kriteri:** Kayıt → Giriş → Çıkış akışı sorunsuz çalışmalı

### OTEL-11: Yetkilendirme Dekoratörleri
- `[ ]` **OTEL-11.1** `utils/decorators.py` — `@role_required('admin')` dekoratörü
- `[ ]` **OTEL-11.2** `utils/decorators.py` — `@hotel_owner_required` dekoratörü
- `[ ]` **OTEL-11.3** Yetkisiz erişimde 403 sayfası
> **Kabul Kriteri:** Normal kullanıcı admin sayfasına erişememeli

### OTEL-12: Auth Templates
- `[ ]` **OTEL-12.1** `templates/auth/login.html` — Login formu
- `[ ]` **OTEL-12.2** `templates/auth/register.html` — Kayıt formu
- `[ ]` **OTEL-12.3** Flash mesaj gösterimi (başarı/hata)
> **Kabul Kriteri:** Formlar responsive, validasyon hataları görünür

🔖 **Commit:** `[OTEL-12] Auth sistemi tamamlandı` → **Push & Tag v0.3.0**

---

## EPIC-4: Otel CRUD, Arama ve Rezervasyon ⚙️ 🟠
**Tag:** `v0.4.0` | **Branch:** `feature/OTEL-epic-4-hotel-crud`

### OTEL-13: Hotel Service Layer
- `[ ]` **OTEL-13.1** `services/hotel_service.py` — create_hotel (validasyon + kayıt)
- `[ ]` **OTEL-13.2** `services/hotel_service.py` — update_hotel (sahiplik kontrolü)
- `[ ]` **OTEL-13.3** `services/hotel_service.py` — search_hotels (şehir, yıldız, fiyat, amenity filtresi)
- `[ ]` **OTEL-13.4** `services/hotel_service.py` — approve_hotel (admin)
- `[ ]` **OTEL-13.5** `services/hotel_service.py` — upload_images (resize + kayıt)
> **Kabul Kriteri:** İş kuralları service'te, DB işleri repository'de olmalı

### OTEL-14: Reservation Service Layer
- `[ ]` **OTEL-14.1** `services/reservation_service.py` — create_reservation (müsaitlik + fiyat hesaplama)
- `[ ]` **OTEL-14.2** `services/reservation_service.py` — cancel_reservation (durum kontrolü)
- `[ ]` **OTEL-14.3** `services/reservation_service.py` — get_user_reservations
> **Kabul Kriteri:** Tarih çakışması engellenmeli, fiyat doğru hesaplanmalı

### OTEL-15: Review Service Layer
- `[ ]` **OTEL-15.1** `services/review_service.py` — add_review (tekrar yorum engelle)
- `[ ]` **OTEL-15.2** `services/review_service.py` — get_hotel_reviews (sayfalama + ortalama puan)
> **Kabul Kriteri:** Bir kullanıcı aynı otele 2 yorum yazamamalı

### OTEL-16: Hotel Forms
- `[ ]` **OTEL-16.1** `forms/hotel_forms.py` — HotelForm (isim, şehir, yıldız, fiyat, açıklama...)
- `[ ]` **OTEL-16.2** `forms/hotel_forms.py` — RoomTypeForm
- `[ ]` **OTEL-16.3** `forms/reservation_forms.py` — ReservationForm (tarih, misafir)
> **Kabul Kriteri:** Validasyon kuralları çalışmalı

### OTEL-17: Public Hotel Routes
- `[ ]` **OTEL-17.1** `routes/hotel.py` — `GET /hotels` (liste + sayfalama)
- `[ ]` **OTEL-17.2** `routes/hotel.py` — `GET /hotels/<id>` (detay)
- `[ ]` **OTEL-17.3** `routes/hotel.py` — `GET /hotels/search` (filtreleme)
- `[ ]` **OTEL-17.4** `routes/hotel.py` — `POST /hotels/<id>/reserve` (login gerekli)
- `[ ]` **OTEL-17.5** `routes/hotel.py` — `POST /hotels/<id>/review` (login gerekli)
> **Kabul Kriteri:** Misafirler otel görebilmeli, giriş yapanlar rezervasyon/yorum yapabilmeli

### OTEL-18: Hotel Owner Routes
- `[ ]` **OTEL-18.1** `routes/hotel_owner.py` — `GET /owner/dashboard`
- `[ ]` **OTEL-18.2** `routes/hotel_owner.py` — `GET/POST /owner/hotel/new`
- `[ ]` **OTEL-18.3** `routes/hotel_owner.py` — `GET/POST /owner/hotel/<id>/edit`
- `[ ]` **OTEL-18.4** `routes/hotel_owner.py` — `POST /owner/hotel/<id>/delete`
- `[ ]` **OTEL-18.5** `routes/hotel_owner.py` — `POST /owner/hotel/<id>/rooms` (oda tipi ekle)
> **Kabul Kriteri:** Otel sahibi sadece kendi otellerini yönetebilmeli

### OTEL-19: Admin Routes
- `[ ]` **OTEL-19.1** `routes/admin.py` — `GET /admin/dashboard` (istatistikler)
- `[ ]` **OTEL-19.2** `routes/admin.py` — `GET /admin/hotels` + `POST approve`
- `[ ]` **OTEL-19.3** `routes/admin.py` — `GET /admin/users` + `POST toggle`
> **Kabul Kriteri:** Sadece admin erişebilmeli, otel onaylama çalışmalı

### OTEL-20: User Dashboard Routes
- `[ ]` **OTEL-20.1** `routes/dashboard.py` — `GET /dashboard` (profil)
- `[ ]` **OTEL-20.2** `routes/dashboard.py` — `GET /dashboard/reservations`
- `[ ]` **OTEL-20.3** `routes/dashboard.py` — `POST /dashboard/reservation/<id>/cancel`
> **Kabul Kriteri:** Kullanıcı kendi rezervasyonlarını görebilmeli ve iptal edebilmeli

🔖 **Commit:** `[OTEL-20] CRUD ve iş mantığı tamamlandı` → **Push & Tag v0.4.0**

---

## EPIC-5: Frontend Tasarımı ve Son Polish 🔴
**Tag:** `v1.0.0` | **Branch:** `feature/OTEL-epic-5-frontend`

### OTEL-21: Tasarım Sistemi
- `[ ]` **OTEL-21.1** `static/css/style.css` — CSS değişkenleri (renkler, tipografi, spacing, shadows)
- `[ ]` **OTEL-21.2** Google Fonts entegrasyonu (Inter / Outfit)
- `[ ]` **OTEL-21.3** Koyu/açık tema CSS desteği
- `[ ]` **OTEL-21.4** Responsive breakpoints (mobile-first)
> **Kabul Kriteri:** Tutarlı renk paleti ve tipografi uygulanmalı

### OTEL-22: Layout ve Bileşenler
- `[ ]` **OTEL-22.1** `templates/base.html` — Ana layout (navbar, content, footer)
- `[ ]` **OTEL-22.2** `templates/components/navbar.html` — Logo, nav, user menü, mobil menü
- `[ ]` **OTEL-22.3** `templates/components/footer.html`
- `[ ]` **OTEL-22.4** `templates/components/hotel_card.html` — Yeniden kullanılabilir kart
- `[ ]` **OTEL-22.5** `templates/components/flash_messages.html`
> **Kabul Kriteri:** Navbar responsive, mobil menü çalışmalı

### OTEL-23: Ana Sayfa
- `[ ]` **OTEL-23.1** `templates/main/index.html` — Hero + arama formu
- `[ ]` **OTEL-23.2** Popüler oteller bölümü
- `[ ]` **OTEL-23.3** Öne çıkan şehirler bölümü
- `[ ]` **OTEL-23.4** `routes/main.py` — Ana sayfa route
> **Kabul Kriteri:** Görsel olarak etkileyici, arama çalışmalı

### OTEL-24: Otel Sayfaları
- `[ ]` **OTEL-24.1** `templates/hotel/list.html` — Filtre paneli + otel grid
- `[ ]` **OTEL-24.2** `templates/hotel/detail.html` — Galeri + bilgi + rezervasyon formu + yorumlar
- `[ ]` **OTEL-24.3** Sıralama (fiyat, puan, yıldız) + sayfalama
> **Kabul Kriteri:** Filtreleme çalışmalı, detay sayfası eksiksiz

### OTEL-25: Dashboard Sayfaları
- `[ ]` **OTEL-25.1** `templates/dashboard/user.html` — Profil + rezervasyonlar
- `[ ]` **OTEL-25.2** `templates/dashboard/owner.html` — Otel yönetim paneli
- `[ ]` **OTEL-25.3** `templates/admin/dashboard.html` — İstatistik kartları + tablolar
- `[ ]` **OTEL-25.4** `templates/admin/hotels.html` + `users.html`
> **Kabul Kriteri:** Her rol kendi panelini görmeli

### OTEL-26: JavaScript ve Etkileşimler
- `[ ]` **OTEL-26.1** `static/js/main.js` — Mobil menü, tema toggle
- `[ ]` **OTEL-26.2** Fotoğraf galerisi (lightbox)
- `[ ]` **OTEL-26.3** Dinamik fiyat hesaplama (gece × fiyat)
- `[ ]` **OTEL-26.4** Client-side form validasyonu
- `[ ]` **OTEL-26.5** Micro-animasyonlar (hover, scroll, fade-in)
> **Kabul Kriteri:** Etkileşimler smooth, performanslı olmalı

### OTEL-27: Son Kontrol ve Deploy Hazırlık
- `[ ]` **OTEL-27.1** Tüm sayfa akışlarını test et
- `[ ]` **OTEL-27.2** Responsive kontrolü (mobil/tablet/desktop)
- `[ ]` **OTEL-27.3** README.md güncelle (kurulum talimatları, ekran görüntüleri)
- `[ ]` **OTEL-27.4** Son commit + Tag v1.0.0
> **Kabul Kriteri:** Tüm akışlar hatasız, responsive, görsel olarak premium

🔖 **Final commit:** `[OTEL-27] v1.0.0 — İlk sürüm` → **Push & Tag v1.0.0**

---

## Özet Tablo

| Epic | Story Sayısı | Task Sayısı | Git Tag |
|------|-------------|-------------|---------|
| EPIC-1: Altyapı | 3 | 11 | v0.1.0 |
| EPIC-2: Data Layer | 4 | 16 | v0.2.0 |
| EPIC-3: Auth | 5 | 14 | v0.3.0 |
| EPIC-4: CRUD & İş Mantığı | 8 | 28 | v0.4.0 |
| EPIC-5: Frontend | 7 | 22 | v1.0.0 |
| **Toplam** | **27 Story** | **91 Task** | — |
