# 🏨 Otel Rezervasyon Web Sitesi — İmplementasyon Planı

Kullanıcıların uygun otelleri arayıp listeleyebildiği, otel sahiplerinin kendi otellerini yönetebildiği ve admin paneli üzerinden tüm sistemin kontrol edilebildiği tam kapsamlı bir otel web sitesi.

**Mimari:** Katmanlı Mimari (Layered Architecture)

---

## Mimari Yaklaşım — Katmanlı Mimari

```mermaid
flowchart TB
    subgraph Presentation["🎨 Presentation Layer"]
        direction LR
        Templates["Jinja2 Templates"]
        Routes["Flask Blueprints<br/>(Routes/Controllers)"]
        Forms["WTForms"]
    end

    subgraph Service["⚙️ Service Layer (İş Mantığı)"]
        direction LR
        AuthService["auth_service"]
        HotelService["hotel_service"]
        ReservationService["reservation_service"]
        ReviewService["review_service"]
    end

    subgraph Repository["🗄️ Repository Layer (Veri Erişim)"]
        direction LR
        UserRepo["user_repository"]
        HotelRepo["hotel_repository"]
        ReservationRepo["reservation_repository"]
        ReviewRepo["review_repository"]
    end

    subgraph Data["💾 Data Layer"]
        direction LR
        Models["SQLAlchemy Models"]
        DB["SQLite / PostgreSQL"]
    end

    Presentation --> Service
    Service --> Repository
    Repository --> Data
```

### Katmanlar Arası Sorumluluk

| Katman | Sorumluluk | Ne yapmaz? |
|--------|------------|------------|
| **Presentation** | HTTP request/response, form validasyonu, template render | İş mantığı, DB sorgusu |
| **Service** | İş kuralları, validasyon, akış kontrolü | DB sorgusu, HTTP işlemi |
| **Repository** | CRUD operasyonları, DB sorguları, filtreleme | İş mantığı, HTTP işlemi |
| **Data (Model)** | Tablo yapısı, ilişkiler, basit hesaplamalar | Hiçbir mantık |

### Örnek Akış — Rezervasyon Oluşturma

```mermaid
sequenceDiagram
    participant U as Kullanıcı
    participant R as Route (Presentation)
    participant S as ReservationService
    participant RR as ReservationRepository
    participant RMR as RoomRepository
    participant DB as Database

    U->>R: POST /hotel/5/reserve (form data)
    R->>R: Form validasyonu (WTForms)
    R->>S: create_reservation(user_id, room_type_id, check_in, check_out, guests)
    S->>RMR: get_room_type(room_type_id)
    RMR->>DB: SELECT room_type
    DB-->>RMR: room_type data
    RMR-->>S: room_type object
    S->>S: Tarih çakışma kontrolü
    S->>S: Fiyat hesaplama (gece * fiyat)
    S->>S: Müsaitlik kontrolü
    S->>RR: save(reservation)
    RR->>DB: INSERT reservation
    DB-->>RR: OK
    RR-->>S: reservation object
    S-->>R: reservation (başarılı)
    R-->>U: Redirect → Rezervasyon onay sayfası
```

---

## Teknoloji Yığını

| Katman | Teknoloji | Neden? |
|--------|-----------|--------|
| **Backend** | Python 3.11+ / Flask | Hafif, esnek, hızlı prototipleme |
| **Veritabanı** | SQLite (dev) → PostgreSQL (prod) | Başlangıç kolay, sonra ölçeklenebilir |
| **ORM** | SQLAlchemy + Flask-Migrate | Veritabanı yönetimi ve migration |
| **Auth** | Flask-Login + Werkzeug | Oturum yönetimi ve şifre hash |
| **Frontend** | Jinja2 + HTML/CSS/JS | Server-side rendering, modern UI |
| **Form** | Flask-WTF / WTForms | CSRF koruması ve form validasyonu |
| **Dosya Upload** | Werkzeug + Pillow | Otel fotoğrafları |

---

## Veritabanı Şeması

```mermaid
erDiagram
    USER {
        int id PK
        string username
        string email
        string password_hash
        string role "user | hotel_owner | admin"
        datetime created_at
        boolean is_active
    }

    HOTEL {
        int id PK
        int owner_id FK
        string name
        string description
        string city
        string address
        int star_rating "1-5"
        float price_min
        float price_max
        string phone
        string email
        boolean is_approved
        boolean is_active
        datetime created_at
    }

    HOTEL_IMAGE {
        int id PK
        int hotel_id FK
        string image_path
        boolean is_primary
        int sort_order
    }

    ROOM_TYPE {
        int id PK
        int hotel_id FK
        string name "Standart, Deluxe, Suite"
        float price_per_night
        int capacity
        int total_rooms
        string description
    }

    AMENITY {
        int id PK
        string name "WiFi, Havuz, SPA"
        string icon
        string category
    }

    HOTEL_AMENITY {
        int hotel_id FK
        int amenity_id FK
    }

    RESERVATION {
        int id PK
        int user_id FK
        int room_type_id FK
        date check_in
        date check_out
        int guests
        float total_price
        string status "pending | confirmed | cancelled"
        datetime created_at
    }

    REVIEW {
        int id PK
        int user_id FK
        int hotel_id FK
        int rating "1-5"
        string comment
        datetime created_at
    }

    USER ||--o{ HOTEL : "owns"
    USER ||--o{ RESERVATION : "makes"
    USER ||--o{ REVIEW : "writes"
    HOTEL ||--o{ HOTEL_IMAGE : "has"
    HOTEL ||--o{ ROOM_TYPE : "has"
    HOTEL ||--o{ HOTEL_AMENITY : "has"
    AMENITY ||--o{ HOTEL_AMENITY : "belongs"
    ROOM_TYPE ||--o{ RESERVATION : "booked"
    HOTEL ||--o{ REVIEW : "receives"
```

---

## Kullanıcı Rolleri ve Yetkileri

| Özellik | Misafir | Kullanıcı | Otel Sahibi | Admin |
|---------|---------|-----------|-------------|-------|
| Otelleri görüntüle | ✅ | ✅ | ✅ | ✅ |
| Otel arama/filtreleme | ✅ | ✅ | ✅ | ✅ |
| Rezervasyon yap | ❌ | ✅ | ✅ | ✅ |
| Yorum yaz | ❌ | ✅ | ❌ | ✅ |
| Otel ekle/düzenle | ❌ | ❌ | ✅ (kendi) | ✅ (tümü) |
| Otel onayla | ❌ | ❌ | ❌ | ✅ |
| Kullanıcı yönetimi | ❌ | ❌ | ❌ | ✅ |

---

## Proje Dizin Yapısı (Katmanlı Mimari)

```
proje_otel/
├── app/
│   ├── __init__.py                  # Application Factory
│   ├── config.py                    # Konfigürasyon sınıfları
│   ├── extensions.py                # Flask eklenti başlatma
│   │
│   ├── models/                      # 💾 DATA LAYER
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── hotel.py
│   │   ├── room.py
│   │   ├── amenity.py
│   │   ├── reservation.py
│   │   └── review.py
│   │
│   ├── repositories/                # 🗄️ REPOSITORY LAYER
│   │   ├── __init__.py
│   │   ├── base_repository.py       # Generic CRUD base class
│   │   ├── user_repository.py
│   │   ├── hotel_repository.py
│   │   ├── room_repository.py
│   │   ├── amenity_repository.py
│   │   ├── reservation_repository.py
│   │   └── review_repository.py
│   │
│   ├── services/                    # ⚙️ SERVICE LAYER
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── hotel_service.py
│   │   ├── reservation_service.py
│   │   └── review_service.py
│   │
│   ├── routes/                      # 🎨 PRESENTATION LAYER
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── auth.py
│   │   ├── hotel.py
│   │   ├── dashboard.py
│   │   ├── hotel_owner.py
│   │   └── admin.py
│   │
│   ├── forms/
│   │   ├── __init__.py
│   │   ├── auth_forms.py
│   │   ├── hotel_forms.py
│   │   └── reservation_forms.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── components/
│   │   │   ├── navbar.html
│   │   │   ├── footer.html
│   │   │   ├── hotel_card.html
│   │   │   └── flash_messages.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── main/
│   │   │   ├── index.html
│   │   │   └── about.html
│   │   ├── hotel/
│   │   │   ├── list.html
│   │   │   ├── detail.html
│   │   │   └── search.html
│   │   ├── dashboard/
│   │   │   ├── user.html
│   │   │   ├── owner.html
│   │   │   └── reservations.html
│   │   └── admin/
│   │       ├── dashboard.html
│   │       ├── hotels.html
│   │       └── users.html
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── main.js
│   │   ├── images/
│   │   └── uploads/
│   │
│   └── utils/
│       ├── __init__.py
│       ├── decorators.py
│       └── helpers.py
│
├── migrations/
├── seed.py                          # Başlangıç verileri
├── .env
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

---

## User Review Required

> [!IMPORTANT]
> **Ödeme sistemi:** Bu planda gerçek ödeme entegrasyonu yok. Rezervasyonlar "onay bekliyor" statüsünde oluşturulacak. Ödeme sistemi istenirse planı güncelleyebilirim.

> [!IMPORTANT]
> **Çoklu dil desteği:** Şu an yalnızca Türkçe planlandı. İngilizce desteği istiyor musunuz?

> [!WARNING]
> **Harita entegrasyonu:** Google Maps veya Leaflet.js ile otel konumu gösterimi dahil edilsin mi?

---

## Open Questions

> [!IMPORTANT]
> 1. **Otel sahibi** ayrı kayıt formundan mı olacak, yoksa mevcut kullanıcı sonradan yükseltilecek mi?
> 2. **E-posta doğrulama** gerekli mi?
> 3. **Tema tercihi:** Koyu mu, açık mı, her ikisi mi?

---

## Verification Plan

### Automated Tests
- Her Epic sonunda `flask run` ile uygulama ayağa kaldırılacak
- Tarayıcıda tüm sayfa akışları kontrol edilecek
- Katmanlar arası veri akışı doğrulanacak

### Manuel Doğrulama
- **EPIC-1:** Uygulama başlatılıyor mu? Boş sayfa geliyor mu?
- **EPIC-2:** Tablolar oluşuyor mu? Repository CRUD çalışıyor mu?
- **EPIC-3:** Kayıt/giriş/çıkış + rol bazlı erişim kontrolü
- **EPIC-4:** Otel CRUD, arama, filtreleme, service layer iş kuralları
- **EPIC-5:** Responsive tasarım, animasyonlar, tema geçişi

### GitHub Push Stratejisi
- Her **Story** tamamlandığında bir commit
- Her **Epic** tamamlandığında bir Git tag (v0.1, v0.2...)
- Commit mesajları: `[OTEL-XX] Story açıklaması`
