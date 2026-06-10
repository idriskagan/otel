# 🏨 Otel Projesi — Jira Task Board

> **Proje Kodu:** OTEL  
> **Git Branch Stratejisi:** `main` ← `develop` ← `feature/OTEL-XX-aciklama`  
> **Commit Format:** `[OTEL-XX] Açıklama`

---

## ~~EPIC-1: Proje Altyapısı ve Konfigürasyon~~ ✅ TAMAMLANDI
**Tag:** `v0.1.0` | **Branch:** `development`

### OTEL-1: Proje İskeleti Oluşturma
- `[x]` **OTEL-1.1** Virtual environment oluştur (`python -m venv venv`)
- `[x]` **OTEL-1.2** `requirements.txt` oluştur (Flask, SQLAlchemy, Migrate, Login, WTF, dotenv, Pillow)
- `[x]` **OTEL-1.3** Bağımlılıkları yükle (`pip install -r requirements.txt`)
- `[x]` **OTEL-1.4** `.gitignore` ve `.env` dosyalarını oluştur
> ✅ **Kabul Kriteri:** `pip freeze` ile tüm paketler yüklü görünmeli

### OTEL-2: Flask Application Factory
- `[x]` **OTEL-2.1** `app/__init__.py` — create_app() factory fonksiyonu
- `[x]` **OTEL-2.2** `app/config.py` — Dev/Prod/Test konfigürasyon sınıfları
- `[x]` **OTEL-2.3** `app/extensions.py` — db, migrate, login_manager init
- `[x]` **OTEL-2.4** `run.py` — Entry point
> ✅ **Kabul Kriteri:** `flask run` ile uygulama başladı, 200 OK döndü

### OTEL-3: Temel Dizin Yapısı
- `[x]` **OTEL-3.1** `models/`, `repositories/`, `services/`, `routes/`, `forms/`, `utils/` klasörleri + `__init__.py`
- `[x]` **OTEL-3.2** `templates/` ve `static/` klasör yapısı
- `[x]` **OTEL-3.3** Minimal `base.html` template + `style.css` placeholder
- `[x]` **OTEL-3.4** `README.md` oluştur
> ✅ **Kabul Kriteri:** Tüm klasörler mevcut, import hataları yok

🔖 **Commit:** `[OTEL-3] Proje altyapısı tamamlandı` → **Push & Tag v0.1.0** ✅

---

## ~~EPIC-2: Data Layer — Modeller ve Repository~~ ✅ TAMAMLANDI
**Tag:** `v0.2.0` | **Branch:** `development`

### OTEL-4: SQLAlchemy Modelleri
- `[x]` **OTEL-4.1** `models/user.py` — User modeli (UserMixin, password hash/check)
- `[x]` **OTEL-4.2** `models/hotel.py` — Hotel + HotelImage modelleri
- `[x]` **OTEL-4.3** `models/room.py` — RoomType modeli
- `[x]` **OTEL-4.4** `models/amenity.py` — Amenity + hotel_amenities M2M tablosu
- `[x]` **OTEL-4.5** `models/reservation.py` — Reservation modeli
- `[x]` **OTEL-4.6** `models/review.py` — Review modeli
- `[x]` **OTEL-4.7** `models/__init__.py` — Tüm modelleri export et
> ✅ **Kabul Kriteri:** `flask db migrate` hatasız çalıştı

### OTEL-5: Base Repository Pattern
- `[x]` **OTEL-5.1** `repositories/base_repository.py` — Generic CRUD (get_by_id, get_all, create, update, delete, paginate)
> ✅ **Kabul Kriteri:** BaseRepository tüm modellerde kullanılabilir durumda

### OTEL-6: Entity Repository'leri
- `[x]` **OTEL-6.1** `repositories/user_repository.py` — get_by_email, get_by_username, get_by_role
- `[x]` **OTEL-6.2** `repositories/hotel_repository.py` — search, filter_by_city, filter_by_stars, get_approved, get_by_owner
- `[x]` **OTEL-6.3** `repositories/room_repository.py` — get_by_hotel, check_availability
- `[x]` **OTEL-6.4** `repositories/amenity_repository.py` — get_all, get_by_category
- `[x]` **OTEL-6.5** `repositories/reservation_repository.py` — get_by_user, get_by_hotel, get_conflicts
- `[x]` **OTEL-6.6** `repositories/review_repository.py` — get_by_hotel, get_average_rating
> ✅ **Kabul Kriteri:** Her repository BaseRepository'den türetildi, özel sorgular yazıldı

### OTEL-7: Migration ve Seed Data
- `[x]` **OTEL-7.1** `flask db init` + `flask db migrate` + `flask db upgrade`
- `[x]` **OTEL-7.2** `seed.py` — Admin kullanıcı, örnek amenity'ler, 3-5 örnek otel
- `[x]` **OTEL-7.3** Seed script'i çalıştır ve doğrula
> ✅ **Kabul Kriteri:** DB oluştu, seed data başarıyla yüklendi

🔖 **Commit:** `[OTEL-7] Data layer tamamlandı` → **Push & Tag v0.2.0** ✅

---

## ~~EPIC-3: Auth Sistemi — Service + Presentation~~ ✅ TAMAMLANDI
<<<<<<< HEAD
**Tag:** `v0.3.0` | **Branch:** `feature/OTEL-epic-3-auth`
=======
**Tag:** `v0.3.0` | **Branch:** `kayit_olma`
>>>>>>> origin/development

### OTEL-8: Auth Service Layer
- `[x]` **OTEL-8.1** `services/auth_service.py` — register_user(data): validasyon + hash + kayıt
- `[x]` **OTEL-8.2** `services/auth_service.py` — login_user(email, password): doğrulama
- `[x]` **OTEL-8.3** `services/auth_service.py` — Hata yönetimi (duplicate email, yanlış şifre)
<<<<<<< HEAD
> **Kabul Kriteri:** Service katmanı route'dan bağımsız test edilebilmeli
=======
> ✅ **Kabul Kriteri:** Service katmanı route'dan bağımsız test edilebilir.
>>>>>>> origin/development

### OTEL-9: Auth Forms
- `[x]` **OTEL-9.1** `forms/auth_forms.py` — LoginForm (email, password, CSRF)
- `[x]` **OTEL-9.2** `forms/auth_forms.py` — RegisterForm (username, email, password, confirm, role)
<<<<<<< HEAD
> **Kabul Kriteri:** Validasyon kuralları (email format, min şifre uzunluğu) çalışmalı
=======
> ✅ **Kabul Kriteri:** Validasyon kuralları (email format, min şifre uzunluğu) çalışıyor.
>>>>>>> origin/development

### OTEL-10: Auth Routes (Presentation)
- `[x]` **OTEL-10.1** `routes/auth.py` — Blueprint tanımla
- `[x]` **OTEL-10.2** `GET/POST /login` — Giriş sayfası
- `[x]` **OTEL-10.3** `GET/POST /register` — Kayıt sayfası (kullanıcı/otel sahibi seçimi)
- `[x]` **OTEL-10.4** `GET /logout` — Çıkış
- `[x]` **OTEL-10.5** Flask-Login user_loader callback
<<<<<<< HEAD
> **Kabul Kriteri:** Kayıt → Giriş → Çıkış akışı sorunsuz çalışmalı
=======
> ✅ **Kabul Kriteri:** Kayıt → Giriş → Çıkış akışı sorunsuz çalışıyor.
>>>>>>> origin/development

### OTEL-11: Yetkilendirme Dekoratörleri
- `[x]` **OTEL-11.1** `utils/decorators.py` — `@role_required('admin')` dekoratörü
- `[x]` **OTEL-11.2** `utils/decorators.py` — `@hotel_owner_required` dekoratörü
<<<<<<< HEAD
- `[x]` **OTEL-11.3** Yetkisiz erişimde 403 sayfası
> **Kabul Kriteri:** Normal kullanıcı admin sayfasına erişememeli
=======
- `[x]` **OTEL-11.3** Yetkisiz erişimde 403 / redirect
> ✅ **Kabul Kriteri:** Yetki bazlı dekoratörler eklendi.
>>>>>>> origin/development

### OTEL-12: Auth Templates
- `[x]` **OTEL-12.1** `templates/auth/login.html` — Login formu
- `[x]` **OTEL-12.2** `templates/auth/register.html` — Kayıt formu
- `[x]` **OTEL-12.3** Flash mesaj gösterimi (başarı/hata)
<<<<<<< HEAD
> **Kabul Kriteri:** Formlar responsive, validasyon hataları görünür
=======
> ✅ **Kabul Kriteri:** Formlar responsive ve validasyon hataları gösteriliyor.
>>>>>>> origin/development

🔖 **Commit:** `[OTEL-12] Auth sistemi tamamlandı` → **Push & Tag v0.3.0** ✅

---

## ~~EPIC-4: Otel CRUD, Arama ve Rezervasyon~~ ✅ TAMAMLANDI
**Tag:** `v0.4.0` | **Branch:** `feature/OTEL-epic-4-hotel-crud`

### OTEL-13: Hotel Service Layer
- `[x]` **OTEL-13.1** `services/hotel_service.py` — create_hotel (validasyon + kayıt)
- `[x]` **OTEL-13.2** `services/hotel_service.py` — update_hotel (sahiplik kontrolü)
- `[x]` **OTEL-13.3** `services/hotel_service.py` — search_hotels (şehir, yıldız, fiyat, amenity filtresi)
- `[x]` **OTEL-13.4** `services/hotel_service.py` — approve_hotel (admin)
- `[x]` **OTEL-13.5** `services/hotel_service.py` — upload_images (resize + kayıt)
> **Kabul Kriteri:** İş kuralları service'te, DB işleri repository'de olmalı

### OTEL-14: Reservation Service Layer
- `[x]` **OTEL-14.1** `services/reservation_service.py` — create_reservation (müsaitlik + fiyat hesaplama)
- `[x]` **OTEL-14.2** `services/reservation_service.py` — cancel_reservation (durum kontrolü)
- `[x]` **OTEL-14.3** `services/reservation_service.py` — get_user_reservations
> **Kabul Kriteri:** Tarih çakışması engellenmeli, fiyat doğru hesaplanmalı

### OTEL-15: Review Service Layer
- `[x]` **OTEL-15.1** `services/review_service.py` — add_review (tekrar yorum engelle)
- `[x]` **OTEL-15.2** `services/review_service.py` — get_hotel_reviews (sayfalama + ortalama puan)
> **Kabul Kriteri:** Bir kullanıcı aynı otele 2 yorum yazamamalı

### OTEL-16: Hotel Forms
- `[x]` **OTEL-16.1** `forms/hotel_forms.py` — HotelForm (isim, şehir, yıldız, fiyat, açıklama...)
- `[x]` **OTEL-16.2** `forms/hotel_forms.py` — RoomTypeForm
- `[x]` **OTEL-16.3** `forms/reservation_forms.py` — ReservationForm (tarih, misafir)
> **Kabul Kriteri:** Validasyon kuralları çalışmalı

### OTEL-17: Public Hotel Routes
- `[x]` **OTEL-17.1** `routes/hotel.py` — `GET /hotels` (liste + sayfalama)
- `[x]` **OTEL-17.2** `routes/hotel.py` — `GET /hotels/<id>` (detay)
- `[x]` **OTEL-17.3** `routes/hotel.py` — `GET /hotels/search` (filtreleme)
- `[x]` **OTEL-17.4** `routes/hotel.py` — `POST /hotels/<id>/reserve` (login gerekli)
- `[x]` **OTEL-17.5** `routes/hotel.py` — `POST /hotels/<id>/review` (login gerekli)
> **Kabul Kriteri:** Misafirler otel görebilmeli, giriş yapanlar rezervasyon/yorum yapabilmeli

### OTEL-18: Hotel Owner Routes
- `[x]` **OTEL-18.1** `routes/hotel_owner.py` — `GET /owner/dashboard`
- `[x]` **OTEL-18.2** `routes/hotel_owner.py` — `GET/POST /owner/hotel/new`
- `[x]` **OTEL-18.3** `routes/hotel_owner.py` — `GET/POST /owner/hotel/<id>/edit`
- `[x]` **OTEL-18.4** `routes/hotel_owner.py` — `POST /owner/hotel/<id>/delete`
- `[x]` **OTEL-18.5** `routes/hotel_owner.py` — `POST /owner/hotel/<id>/rooms` (oda tipi ekle)
> **Kabul Kriteri:** Otel sahibi sadece kendi otellerini yönetebilmeli

### OTEL-19: Admin Routes
- `[x]` **OTEL-19.1** `routes/admin.py` — `GET /admin/dashboard` (istatistikler)
- `[x]` **OTEL-19.2** `routes/admin.py` — `GET /admin/hotels` + `POST approve`
- `[x]` **OTEL-19.3** `routes/admin.py` — `GET /admin/users` + `POST toggle`
> **Kabul Kriteri:** Sadece admin erişebilmeli, otel onaylama çalışmalı

### OTEL-20: User Dashboard Routes
- `[x]` **OTEL-20.1** `routes/dashboard.py` — `GET /dashboard` (profil)
- `[x]` **OTEL-20.2** `routes/dashboard.py` — `GET /dashboard/reservations`
- `[x]` **OTEL-20.3** `routes/dashboard.py` — `POST /dashboard/reservation/<id>/cancel`
> **Kabul Kriteri:** Kullanıcı kendi rezervasyonlarını görebilmeli ve iptal edebilmeli

🔖 **Commit:** `[OTEL-20] CRUD ve iş mantığı tamamlandı` → **Push & Tag v0.4.0** ✅

---

## ~~EPIC-5: Frontend Tasarımı ve Son Polish~~ ✅ TAMAMLANDI
**Tag:** `v1.0.0` | **Branch:** `feature/OTEL-epic-5-frontend`

### OTEL-21: Tasarım Sistemi
- `[x]` **OTEL-21.1** `static/css/style.css` — CSS değişkenleri (renkler, tipografi, spacing, shadows)
- `[x]` **OTEL-21.2** Google Fonts entegrasyonu (Inter / Outfit)
- `[x]` **OTEL-21.3** Koyu/açık tema CSS desteği
- `[x]` **OTEL-21.4** Responsive breakpoints (mobile-first)
> **Kabul Kriteri:** Tutarlı renk paleti ve tipografi uygulanmalı

### OTEL-22: Layout ve Bileşenler
- `[x]` **OTEL-22.1** `templates/base.html` — Ana layout (navbar, content, footer)
- `[x]` **OTEL-22.2** `templates/components/navbar.html` — Logo, nav, user menü, mobil menü
- `[x]` **OTEL-22.3** `templates/components/footer.html`
- `[x]` **OTEL-22.4** `templates/components/hotel_card.html` — Yeniden kullanılabilir kart
- `[x]` **OTEL-22.5** `templates/components/flash_messages.html`
> **Kabul Kriteri:** Navbar responsive, mobil menü çalışmalı

### OTEL-23: Ana Sayfa
- `[x]` **OTEL-23.1** `templates/main/index.html` — Hero + arama formu
- `[x]` **OTEL-23.2** Popüler oteller bölümü
- `[x]` **OTEL-23.3** Öne çıkan şehirler bölümü
- `[x]` **OTEL-23.4** `routes/main.py` — Ana sayfa route
> **Kabul Kriteri:** Görsel olarak etkileyici, arama çalışmalı

### OTEL-24: Otel Sayfaları
- `[x]` **OTEL-24.1** `templates/hotel/list.html` — Filtre paneli + otel grid
- `[x]` **OTEL-24.2** `templates/hotel/detail.html` — Galeri + bilgi + rezervasyon formu + yorumlar
- `[x]` **OTEL-24.3** Sıralama (fiyat, puan, yıldız) + sayfalama
> **Kabul Kriteri:** Filtreleme çalışmalı, detay sayfası eksiksiz

### OTEL-25: Dashboard Sayfaları
- `[x]` **OTEL-25.1** `templates/dashboard/user.html` — Profil + rezervasyonlar
- `[x]` **OTEL-25.2** `templates/dashboard/owner.html` — Otel yönetim paneli
- `[x]` **OTEL-25.3** `templates/admin/dashboard.html` — İstatistik kartları + tablolar
- `[x]` **OTEL-25.4** `templates/admin/hotels.html` + `users.html`
> **Kabul Kriteri:** Her rol kendi panelini görmeli

### OTEL-26: JavaScript ve Etkileşimler
- `[x]` **OTEL-26.1** `static/js/main.js` — Mobil menü hamburger toggle
- `[x]` **OTEL-26.2** Flash mesajlar otomatik kapanma (5sn) ve çarpı butonu
- `[x]` **OTEL-26.3** Dinamik fiyat hesaplama (gece × fiyat)
- `[x]` **OTEL-26.4** Client-side form validasyonu (date check)
- `[x]` **OTEL-26.5** CSS animasyonlar (fadeIn, slideIn, pulse-glow)
> **Kabul Kriteri:** Etkileşimler smooth, performanslı olmalı

### OTEL-27: Son Kontrol ve Deploy Hazırlık
- `[x]` **OTEL-27.1** Tüm sayfa akışları implementasyon tamamlandı
- `[x]` **OTEL-27.2** Responsive breakpoints CSS'e eklendi (mobile-first)
- `[x]` **OTEL-27.3** README.md güncellendi (kurulum talimatları, mimari, sürüm geçmişi)
- `[x]` **OTEL-27.4** Son commit + Tag v1.0.0 hazır
> **Kabul Kriteri:** Tüm akışlar hatasız, responsive, görsel olarak premium

🔖 **Final commit:** `[OTEL-27] v1.0.0 — İlk sürüm` → **Push & Tag v1.0.0** ✅

---

## 🚀 POST v1.0.0 — Geliştirme Yol Haritası

> Aşağıdaki EPIC'ler v1.0.0 sonrasında projeye eklenebilecek özelliklerdir.
> Öncelik sırasına göre listelenmiştir.

---

## EPIC-6: Kullanıcı Deneyimi İyileştirmeleri
**Hedef Tag:** `v1.1.0` | **Branch:** `feature/OTEL-epic-6-ux`

### OTEL-28: Profil Yönetimi ve Ayarlar
- `[x]` **OTEL-28.1** `forms/profile_forms.py` — ProfileUpdateForm (ad, soyad, telefon, avatar)
- `[x]` **OTEL-28.2** `models/user.py` — User modeline `first_name`, `last_name`, `phone`, `avatar_path`, `bio` alanları ekle
- `[x]` **OTEL-28.3** `services/user_service.py` — [YENİ] update_profile, change_password fonksiyonları
- `[x]` **OTEL-28.4** `routes/dashboard.py` — `GET/POST /dashboard/profile/edit` profil düzenleme route
- `[x]` **OTEL-28.5** `templates/dashboard/profile_edit.html` — Profil düzenleme formu (avatar yükleme dahil)
- `[x]` **OTEL-28.6** Şifre değiştirme sayfası (`/dashboard/change-password`)
> **Kabul Kriteri:** Kullanıcı kendi profilini düzenleyebilmeli, avatar yükleyebilmeli, şifre değiştirebilmeli

### OTEL-29: Favoriler / İstek Listesi Sistemi
- `[x]` **OTEL-29.1** `models/favorite.py` — [YENİ] Favorite modeli (user_id, hotel_id, created_at)
- `[x]` **OTEL-29.2** `repositories/favorite_repository.py` — [YENİ] get_by_user, is_favorited, toggle
- `[x]` **OTEL-29.3** `services/favorite_service.py` — [YENİ] toggle_favorite, get_user_favorites
- `[x]` **OTEL-29.4** `routes/dashboard.py` — `POST /dashboard/favorite/<id>` toggle + `GET /dashboard/favorites` liste
- `[x]` **OTEL-29.5** Otel kartı ve detay sayfasına ❤️ favori butonu ekle (AJAX)
- `[x]` **OTEL-29.6** `templates/dashboard/favorites.html` — Favori oteller sayfası
> **Kabul Kriteri:** Kullanıcı otel favoriye alıp çıkarabilmeli, favorilerini listeleyebilmeli

### OTEL-30: Gelişmiş Arama ve Filtreleme
- `[x]` **OTEL-30.1** Fiyat aralığı filtresi (min-max slider veya input) frontend'e ekle
- `[x]` **OTEL-30.2** Amenity bazlı filtreleme (checkbox group) — backend `hotel_repository.search()` güncelle
- `[x]` **OTEL-30.3** Tarih bazlı müsaitlik filtresi (check-in/check-out tarihine göre boş otelleri göster)
- `[x]` **OTEL-30.4** Autocomplete şehir arama (JavaScript + endpoint)
- `[x]` **OTEL-30.5** `templates/hotel/list.html` — Gelişmiş filtre paneli sidebar tasarımı
- `[x]` **OTEL-30.6** URL query parametreleri ile filtrelerin korunması (sayfa yenilemede kaybolmamalı)
> **Kabul Kriteri:** Kullanıcılar fiyat, amenity, tarih ve şehir bazlı gelişmiş arama yapabilmeli

### OTEL-31: Yorum ve Değerlendirme İyileştirmeleri
- `[x]` **OTEL-31.1** Yorum düzenleme ve silme özelliği (kullanıcı kendi yorumunu düzenleyebilmeli)
- `[x]` **OTEL-31.2** Yorum yanıtlama — Otel sahibi yorumlara cevap verebilmeli
- `[x]` **OTEL-31.3** `models/review.py` — `parent_id` alanı ekle (yanıt ilişkisi), `is_edited` flag
- `[x]` **OTEL-31.4** Yorumları sıralama (en yeni, en eski, en yüksek puan, en düşük puan)
- `[x]` **OTEL-31.5** Yorum faydalılık oylama ("Bu yorum faydalı mıydı?" 👍/👎)
> **Kabul Kriteri:** Yorumlar düzenlenebilmeli, otel sahibi yanıt verebilmeli, sıralama çalışmalı

🔖 **Commit:** `[OTEL-31] Kullanıcı deneyimi iyileştirmeleri` → **Push & Tag v1.1.0**

---

## EPIC-7: Bildirim ve İletişim Sistemi
**Hedef Tag:** `v1.2.0` | **Branch:** `feature/OTEL-epic-7-notifications`

### OTEL-32: E-posta Bildirimleri
- `[ ]` **OTEL-32.1** `requirements.txt` — Flask-Mail bağımlılığı ekle
- `[ ]` **OTEL-32.2** `extensions.py` — Mail instance başlat, `config.py`'ye SMTP ayarları ekle
- `[ ]` **OTEL-32.3** `services/email_service.py` — [YENİ] send_email() temel fonksiyon
- `[ ]` **OTEL-32.4** Rezervasyon onay e-postası (kullanıcıya)
- `[ ]` **OTEL-32.5** Yeni rezervasyon bildirim e-postası (otel sahibine)
- `[ ]` **OTEL-32.6** E-posta doğrulama sistemi (kayıt sonrası onay linki)
- `[ ]` **OTEL-32.7** Şifre sıfırlama e-postası (forgot password flow)
- `[ ]` **OTEL-32.8** HTML e-posta template'leri (`templates/email/` klasörü)
> **Kabul Kriteri:** Rezervasyon, kayıt, şifre sıfırlama için otomatik e-postalar gitmeli

### OTEL-33: Uygulama İçi Bildirim Sistemi
- `[ ]` **OTEL-33.1** `models/notification.py` — [YENİ] Notification modeli (user_id, type, message, is_read, created_at)
- `[ ]` **OTEL-33.2** `repositories/notification_repository.py` — [YENİ] get_unread, mark_as_read, mark_all_read
- `[ ]` **OTEL-33.3** `services/notification_service.py` — [YENİ] create_notification, get_user_notifications
- `[ ]` **OTEL-33.4** Navbar'a bildirim ikonu + okunmamış sayı badge ekle
- `[ ]` **OTEL-33.5** `routes/notification.py` — [YENİ] `GET /notifications` + `POST /notifications/<id>/read`
- `[ ]` **OTEL-33.6** `templates/dashboard/notifications.html` — Bildirim listesi sayfası
- `[ ]` **OTEL-33.7** Bildirim tetikleyicileri: rezervasyon onayı, yorum geldi, otel onaylandı vb.
> **Kabul Kriteri:** Kullanıcılar sistem bildirimleri alabilmeli, okundu/okunmadı takibi yapılabilmeli

### OTEL-34: İletişim Formu ve Destek
- `[ ]` **OTEL-34.1** `models/contact.py` — [YENİ] ContactMessage modeli (name, email, subject, message, status)
- `[ ]` **OTEL-34.2** `forms/contact_forms.py` — [YENİ] ContactForm
- `[ ]` **OTEL-34.3** `routes/main.py` — `GET/POST /contact` iletişim sayfası
- `[ ]` **OTEL-34.4** `templates/main/contact.html` — İletişim formu sayfası
- `[ ]` **OTEL-34.5** Admin paneline gelen mesajları listeleme + yanıtlama (`/admin/messages`)
> **Kabul Kriteri:** Ziyaretçiler iletişim formu doldurabilmeli, admin mesajları görebilmeli

🔖 **Commit:** `[OTEL-34] Bildirim ve iletişim sistemi` → **Push & Tag v1.2.0**

---

## EPIC-8: Admin Paneli Geliştirmeleri ve Raporlama
**Hedef Tag:** `v1.3.0` | **Branch:** `feature/OTEL-epic-8-admin-advanced`

### OTEL-35: Gelişmiş Admin Dashboard
- `[ ]` **OTEL-35.1** Dashboard'a gelir raporu (aylık/haftalık/günlük toplam rezervasyon tutarı)
- `[ ]` **OTEL-35.2** Chart.js veya benzeri kütüphane ile grafikler (rezervasyon trendi, gelir grafiği)
- `[ ]` **OTEL-35.3** Son aktiviteler feed'i (son kayıtlar, son rezervasyonlar, son yorumlar)
- `[ ]` **OTEL-35.4** Otel onay bekleyenler widget'ı (hızlı onay/reddet butonları)
- `[ ]` **OTEL-35.5** Kullanıcı istatistikleri (aktif/pasif, role dağılımı pie chart)
> **Kabul Kriteri:** Admin dashboard grafikler ve detaylı istatistikler içermeli

### OTEL-36: Otel Onay Süreci İyileştirme
- `[ ]` **OTEL-36.1** Otel reddetme özelliği + red sebebi mesajı (rejection_reason alanı)
- `[ ]` **OTEL-36.2** Otel sahibine onay/red bildirim e-postası gönder
- `[ ]` **OTEL-36.3** Onay geçmişi log'u (kim, ne zaman onayladı/reddetti)
- `[ ]` **OTEL-36.4** Admin notları — otele admin notu bırakabilme
> **Kabul Kriteri:** Admin otelleri onaylayabilmeli/reddedebilmeli, süreç kayıt altında olmalı

### OTEL-37: Rezervasyon Yönetimi (Admin + Owner)
- `[ ]` **OTEL-37.1** Otel sahibi paneline rezervasyon listesi (kendi otellerine gelen)
- `[ ]` **OTEL-37.2** Rezervasyon onaylama/reddetme (otel sahibi tarafından)
- `[ ]` **OTEL-37.3** Admin paneline tüm rezervasyonları filtreleme/arama
- `[ ]` **OTEL-37.4** Rezervasyon detay sayfası (misafir bilgileri, oda, tarih, fiyat)
- `[ ]` **OTEL-37.5** Rezervasyon durumu geçişleri: pending → confirmed → checked_in → checked_out → cancelled
- `[ ]` **OTEL-37.6** Check-in / Check-out tarihi yaklaşan rezervasyonlar uyarı sistemi
> **Kabul Kriteri:** Otel sahibi rezervasyonları onaylayabilmeli, durum geçişleri çalışmalı

### OTEL-38: Toplu İşlemler ve Veri Dışa Aktarma
- `[ ]` **OTEL-38.1** Admin — Toplu otel onaylama (checkbox + batch approve)
- `[ ]` **OTEL-38.2** Admin — Kullanıcı listesini CSV/Excel dışa aktarma
- `[ ]` **OTEL-38.3** Admin — Rezervasyon raporunu CSV dışa aktarma (tarih aralığı filtresi ile)
- `[ ]` **OTEL-38.4** Otel sahibi — Kendi otellerinin gelir raporunu dışa aktarma
> **Kabul Kriteri:** Admin verileri dışa aktarabilmeli, toplu işlemler çalışmalı

🔖 **Commit:** `[OTEL-38] Admin paneli geliştirmeleri` → **Push & Tag v1.3.0**

---

## EPIC-9: Güvenlik, Performans ve Altyapı
**Hedef Tag:** `v1.4.0` | **Branch:** `feature/OTEL-epic-9-security-perf`

### OTEL-39: Güvenlik İyileştirmeleri
- `[ ]` **OTEL-39.1** Rate limiting (Flask-Limiter) — Login brute-force koruması
- `[ ]` **OTEL-39.2** Güçlü şifre politikası (büyük harf, küçük harf, rakam, özel karakter zorunluluğu)
- `[ ]` **OTEL-39.3** Oturum yönetimi iyileştirme (session timeout, concurrent login kontrolü)
- `[ ]` **OTEL-39.4** XSS koruması — Kullanıcı girdilerinin sanitize edilmesi (bleach veya benzeri)
- `[ ]` **OTEL-39.5** SQL injection koruması doğrulaması (tüm sorgular parametrik mi?)
- `[ ]` **OTEL-39.6** HTTPS zorunluluğu (production) + Secure cookie flags
- `[ ]` **OTEL-39.7** `utils/validators.py` — [YENİ] Merkezi input validasyon fonksiyonları
> **Kabul Kriteri:** OWASP Top 10 güvenlik açıkları kontrol edilmiş olmalı

### OTEL-40: Performans Optimizasyonları
- `[ ]` **OTEL-40.1** Veritabanı sorgu optimizasyonu — N+1 sorgu problemlerini çöz (eager loading)
- `[ ]` **OTEL-40.2** Resim optimizasyonu — Pillow ile upload sırasında otomatik resize + webp dönüşümü
- `[ ]` **OTEL-40.3** Statik dosya cache headers (CSS/JS versiyonlama — cache busting)
- `[ ]` **OTEL-40.4** Veritabanı indeksleri gözden geçir (sık kullanılan sorgu alanlarına index ekle)
- `[ ]` **OTEL-40.5** Lazy loading — Otel listesi ve görseller için infinite scroll veya lazy image loading
- `[ ]` **OTEL-40.6** Gzip compression middleware
> **Kabul Kriteri:** Sayfa yükleme süreleri ölçülmeli, N+1 sorgu kalmamalı

### OTEL-41: Loglama ve Hata Yönetimi
- `[ ]` **OTEL-41.1** `utils/logger.py` — [YENİ] Merkezi loglama konfigürasyonu (file + console handler)
- `[ ]` **OTEL-41.2** Tüm service katmanlarına yapılandırılmış loglama ekle
- `[ ]` **OTEL-41.3** Custom error handler sayfaları (400, 403, 404, 500) — güzel tasarımlı hata sayfaları
- `[ ]` **OTEL-41.4** Exception middleware — beklenmeyen hataları logla ve kullanıcıya anlamlı mesaj göster
- `[ ]` **OTEL-41.5** Request/Response logging middleware (geliştirme ortamı için)
> **Kabul Kriteri:** Tüm hatalar loglanmalı, kullanıcı dostu hata sayfaları gösterilmeli

### OTEL-42: Test Altyapısı
- `[ ]` **OTEL-42.1** `tests/` dizin yapısı oluştur (`tests/unit/`, `tests/integration/`)
- `[ ]` **OTEL-42.2** `pytest` + `pytest-cov` bağımlılıkları ekle
- `[ ]` **OTEL-42.3** `tests/conftest.py` — Test fixtures (app, client, db, auth helpers)
- `[ ]` **OTEL-42.4** Repository katmanı unit testleri (CRUD operasyonları)
- `[ ]` **OTEL-42.5** Service katmanı unit testleri (iş kuralları)
- `[ ]` **OTEL-42.6** Route katmanı integration testleri (HTTP status code, redirect kontrolleri)
- `[ ]` **OTEL-42.7** Auth akışı end-to-end testleri (kayıt → giriş → yetkili erişim → çıkış)
> **Kabul Kriteri:** Minimum %70 test coverage, tüm kritik akışlar test edilmiş olmalı

🔖 **Commit:** `[OTEL-42] Güvenlik ve performans` → **Push & Tag v1.4.0**

---

## EPIC-10: Gelişmiş Özellikler ve Entegrasyonlar
**Hedef Tag:** `v2.0.0` | **Branch:** `feature/OTEL-epic-10-advanced`

### OTEL-43: Harita Entegrasyonu
- `[ ]` **OTEL-43.1** Leaflet.js kütüphanesini projeye ekle (CDN)
- `[ ]` **OTEL-43.2** `models/hotel.py` — `latitude`, `longitude` alanları ekle
- `[ ]` **OTEL-43.3** Otel ekleme/düzenleme formuna harita üzerinden konum seçme
- `[ ]` **OTEL-43.4** Otel detay sayfasına harita embed (konum gösterimi)
- `[ ]` **OTEL-43.5** Otel arama sayfasına harita görünümü (tüm sonuçlar haritada marker ile)
- `[ ]` **OTEL-43.6** "Yakınımdaki Oteller" özelliği (tarayıcı geolocation API)
> **Kabul Kriteri:** Oteller haritada görüntülenebilmeli, konum seçimi çalışmalı

### OTEL-44: REST API Katmanı
- `[ ]` **OTEL-44.1** `routes/api/` — [YENİ] API Blueprint yapısı (v1 prefix)
- `[ ]` **OTEL-44.2** `GET /api/v1/hotels` — Otelleri JSON listele (filtreleme + sayfalama)
- `[ ]` **OTEL-44.3** `GET /api/v1/hotels/<id>` — Otel detay JSON
- `[ ]` **OTEL-44.4** `POST /api/v1/auth/login` — JWT tabanlı kimlik doğrulama
- `[ ]` **OTEL-44.5** `POST /api/v1/reservations` — API üzerinden rezervasyon oluşturma
- `[ ]` **OTEL-44.6** API rate limiting ve authentication middleware
- `[ ]` **OTEL-44.7** Swagger/OpenAPI dokümantasyonu (flask-restx veya flasgger)
> **Kabul Kriteri:** Mobil uygulama veya 3. parti entegrasyonlar için kullanılabilir REST API

### OTEL-45: Çoklu Dil Desteği (i18n)
- `[ ]` **OTEL-45.1** Flask-Babel bağımlılığı ekle ve yapılandır
- `[ ]` **OTEL-45.2** Template'lerde tüm statik metinleri `_()` (gettext) ile sar
- `[ ]` **OTEL-45.3** Türkçe (tr) ve İngilizce (en) çeviri dosyaları oluştur (`translations/`)
- `[ ]` **OTEL-45.4** Dil seçici bileşeni (navbar'da bayrak/dropdown)
- `[ ]` **OTEL-45.5** Kullanıcı dil tercihi kaydetme (User modeline `language` alanı)
- `[ ]` **OTEL-45.6** Tarih/para birimi formatlarını locale'e göre ayarla
> **Kabul Kriteri:** Uygulama Türkçe ve İngilizce olarak kullanılabilmeli

### OTEL-46: Ödeme Sistemi Entegrasyonu
- `[ ]` **OTEL-46.1** Ödeme modeli — `models/payment.py` (transaction_id, amount, status, method)
- `[ ]` **OTEL-46.2** Stripe veya İyzico sandbox entegrasyonu
- `[ ]` **OTEL-46.3** `services/payment_service.py` — [YENİ] create_payment, verify_payment, refund
- `[ ]` **OTEL-46.4** Rezervasyon akışına ödeme adımı ekle
- `[ ]` **OTEL-46.5** Ödeme başarılı/başarısız callback sayfaları
- `[ ]` **OTEL-46.6** Fatura/dekont oluşturma ve PDF indirme
> **Kabul Kriteri:** Sandbox ortamında ödeme akışı çalışmalı, fatura oluşturulmalı

### OTEL-47: Gelişmiş Otel Sahibi Paneli
- `[ ]` **OTEL-47.1** Gelir dashboard'u — Aylık/yıllık gelir grafikleri (kendi otelleri için)
- `[ ]` **OTEL-47.2** Doluluk oranı raporu (oda tipi bazında yüzdesel)
- `[ ]` **OTEL-47.3** Misafir demografik bilgileri ve tekrar ziyaret istatistikleri
- `[ ]` **OTEL-47.4** Dinamik fiyatlandırma — Sezon/tarih bazlı fiyat ayarlama
- `[ ]` **OTEL-47.5** Promosyon/İndirim kodu sistemi (kupon oluşturma)
- `[ ]` **OTEL-47.6** Oda müsaitlik takvimi (calendar view — hangi odalar ne zaman dolu)
> **Kabul Kriteri:** Otel sahibi detaylı raporlara erişebilmeli, dinamik fiyat belirleyebilmeli

🔖 **Commit:** `[OTEL-47] Gelişmiş özellikler tamamlandı` → **Push & Tag v2.0.0**

---

## Özet Tablo

| Epic | Story Sayısı | Task Sayısı | Git Tag | Durum |
|------|-------------|-------------|---------|-------|
| EPIC-1: Altyapı | 3 | 11 | v0.1.0 | ✅ Tamamlandı |
| EPIC-2: Data Layer | 4 | 16 | v0.2.0 | ✅ Tamamlandı |
| EPIC-3: Auth | 5 | 14 | v0.3.0 | ✅ Tamamlandı |
| EPIC-4: CRUD & İş Mantığı | 8 | 28 | v0.4.0 | ✅ Tamamlandı |
| EPIC-5: Frontend | 7 | 22 | v1.0.0 | ✅ Tamamlandı |
| **v1.0.0 Toplam** | **27 Story** | **91 Task** | — | **%100 TAMAMLANDI** |
| | | | | |
| EPIC-6: UX İyileştirmeleri | 4 | 22 | v1.1.0 | 📋 Planlandı |
| EPIC-7: Bildirim & İletişim | 3 | 20 | v1.2.0 | 📋 Planlandı |
| EPIC-8: Admin Geliştirmeleri | 4 | 19 | v1.3.0 | 📋 Planlandı |
| EPIC-9: Güvenlik & Performans | 4 | 24 | v1.4.0 | 📋 Planlandı |
| EPIC-10: Gelişmiş Özellikler | 5 | 32 | v2.0.0 | 📋 Planlandı |
| **Genel Toplam** | **47 Story** | **208 Task** | — | **v1.0.0 ✅ / v2.0.0 📋** |
