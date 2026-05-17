"""
OTEL-7.2: Seed Script — Başlangıç verileri
Çalıştır: python seed.py
"""
from app import create_app
from app.extensions import db
from app.models import User, Hotel, HotelImage, RoomType, Amenity, Review

app = create_app()


def seed_amenities():
    """Otel özelliklerini ekler."""
    amenities_data = [
        {'name': 'Ücretsiz WiFi', 'icon': '📶', 'category': 'iletisim'},
        {'name': 'Açık Yüzme Havuzu', 'icon': '🏊', 'category': 'eglence'},
        {'name': 'Kapalı Yüzme Havuzu', 'icon': '🏊', 'category': 'eglence'},
        {'name': 'SPA & Wellness', 'icon': '💆', 'category': 'saglik'},
        {'name': 'Fitness Merkezi', 'icon': '🏋️', 'category': 'saglik'},
        {'name': 'Restoran', 'icon': '🍽️', 'category': 'yiyecek'},
        {'name': 'Bar & Lounge', 'icon': '🍹', 'category': 'yiyecek'},
        {'name': 'Kahvaltı Dahil', 'icon': '☕', 'category': 'yiyecek'},
        {'name': 'Otopark', 'icon': '🚗', 'category': 'ulasim'},
        {'name': 'Havalimanı Transferi', 'icon': '✈️', 'category': 'ulasim'},
        {'name': 'Oda Servisi', 'icon': '🛎️', 'category': 'hizmet'},
        {'name': 'Çamaşırhane', 'icon': '👕', 'category': 'hizmet'},
        {'name': 'Konferans Salonu', 'icon': '🏢', 'category': 'is'},
        {'name': 'Plaj Erişimi', 'icon': '🏖️', 'category': 'eglence'},
        {'name': 'Çocuk Kulübü', 'icon': '🧒', 'category': 'eglence'},
        {'name': 'Evcil Hayvan Dostu', 'icon': '🐾', 'category': 'genel'},
    ]
    for data in amenities_data:
        if not Amenity.query.filter_by(name=data['name']).first():
            db.session.add(Amenity(**data))
    db.session.commit()
    print(f"Bitti: {len(amenities_data)} amenity eklendi.")


def seed_admin():
    """Admin kullanıcı oluşturur."""
    if not User.query.filter_by(email='admin@stayfinder.com').first():
        admin = User(username='admin', email='admin@stayfinder.com', role='admin')
        admin.set_password('Admin123!')
        db.session.add(admin)
        db.session.commit()
        print("Bitti: Admin kullanıcı oluşturuldu.")
        return admin
    print("Bilgi: Admin zaten mevcut.")
    return User.query.filter_by(email='admin@stayfinder.com').first()


def seed_hotel_owner():
    """Örnek otel sahibi kullanıcı oluşturur."""
    if not User.query.filter_by(email='owner@stayfinder.com').first():
        owner = User(username='otelci', email='owner@stayfinder.com', role='hotel_owner')
        owner.set_password('Owner123!')
        db.session.add(owner)
        db.session.commit()
        print("Bitti: Otel sahibi kullanıcı oluşturuldu.")
        return owner
    return User.query.filter_by(email='owner@stayfinder.com').first()


def seed_sample_user():
    """Örnek misafir kullanıcı oluşturur."""
    if not User.query.filter_by(email='user@stayfinder.com').first():
        user = User(username='misafir', email='user@stayfinder.com', role='user')
        user.set_password('User123!')
        db.session.add(user)
        db.session.commit()
        print("Bitti: Örnek kullanıcı oluşturuldu.")
        return user
    return User.query.filter_by(email='user@stayfinder.com').first()


def seed_hotels(owner):
    """Örnek oteller ekler."""
    wifi = Amenity.query.filter_by(name='Ücretsiz WiFi').first()
    havuz = Amenity.query.filter_by(name='Açık Yüzme Havuzu').first()
    restoran = Amenity.query.filter_by(name='Restoran').first()
    spa = Amenity.query.filter_by(name='SPA & Wellness').first()
    kahvalti = Amenity.query.filter_by(name='Kahvaltı Dahil').first()

    hotels_data = [
        {
            'name': 'Grand İstanbul Palace',
            'city': 'İstanbul',
            'address': 'Taksim Meydanı, Beyoğlu, İstanbul',
            'description': 'İstanbul\'un kalbinde, Taksim\'e yürüme mesafesinde 5 yıldızlı lüks otel. Boğaz manzaralı odalar, üst düzey SPA merkezi ve dünya mutfağından lezzetler.',
            'star_rating': 5,
            'price_min': 1500,
            'price_max': 5000,
            'phone': '+90 212 555 0001',
            'email': 'info@grandistanbul.com',
            'amenities': [wifi, havuz, restoran, spa, kahvalti],
            'rooms': [
                {'name': 'Standart Oda', 'price_per_night': 1500, 'capacity': 2, 'total_rooms': 50},
                {'name': 'Deluxe Oda', 'price_per_night': 2500, 'capacity': 2, 'total_rooms': 30},
                {'name': 'Suite', 'price_per_night': 5000, 'capacity': 4, 'total_rooms': 10},
            ]
        },
        {
            'name': 'Antalya Sahil Resort',
            'city': 'Antalya',
            'address': 'Konyaaltı Sahili, Antalya',
            'description': 'Akdeniz\'in berrak sularına sıfır konumda, all-inclusive hizmet anlayışıyla 4 yıldızlı tatil köyü. Geniş bahçesi ve çocuk aktiviteleriyle ailelerin gözdesi.',
            'star_rating': 4,
            'price_min': 800,
            'price_max': 2500,
            'phone': '+90 242 555 0002',
            'email': 'info@antalyasahil.com',
            'amenities': [wifi, havuz, restoran, kahvalti],
            'rooms': [
                {'name': 'Standart Oda', 'price_per_night': 800, 'capacity': 2, 'total_rooms': 80},
                {'name': 'Aile Odası', 'price_per_night': 1500, 'capacity': 4, 'total_rooms': 30},
            ]
        },
        {
            'name': 'İzmir Butik Otel',
            'city': 'İzmir',
            'address': 'Alsancak, İzmir',
            'description': 'Kordon\'a yürüme mesafesinde, tarihi binada yer alan şık butik otel. Özgün tasarımı ve samimi atmosferiyle unutulmaz bir konaklama deneyimi.',
            'star_rating': 3,
            'price_min': 500,
            'price_max': 1200,
            'phone': '+90 232 555 0003',
            'email': 'info@izmirbutik.com',
            'amenities': [wifi, kahvalti, restoran],
            'rooms': [
                {'name': 'Standart Oda', 'price_per_night': 500, 'capacity': 2, 'total_rooms': 20},
                {'name': 'Deluxe Oda', 'price_per_night': 1200, 'capacity': 2, 'total_rooms': 8},
            ]
        },
        {
            'name': 'Kapadokya Cave Hotel',
            'city': 'Nevşehir',
            'address': 'Göreme, Nevşehir',
            'description': 'Tarihi Göreme\'de, volkanik kayalara oyulmuş eşsiz mağara otel. Sabah balonlu uçuş manzarası ve otantik Kapadokya mutfağıyla unutulmaz deneyim.',
            'star_rating': 5,
            'price_min': 2000,
            'price_max': 6000,
            'phone': '+90 384 555 0004',
            'email': 'info@kapadokyacave.com',
            'amenities': [wifi, spa, restoran, kahvalti],
            'rooms': [
                {'name': 'Mağara Oda', 'price_per_night': 2000, 'capacity': 2, 'total_rooms': 10},
                {'name': 'Lüks Mağara Suite', 'price_per_night': 6000, 'capacity': 2, 'total_rooms': 5},
            ]
        },
        {
            'name': 'Bodrum Blue Escape',
            'city': 'Muğla',
            'address': 'Yalıkavak, Bodrum, Muğla',
            'description': 'Ege\'nin en güzel koylarından Yalıkavak\'ta denize sıfır lüks tatil tesisi. Marinaya yakın konumu ve Yunan adaları manzarasıyla ayrıcalıklı bir kaçış.',
            'star_rating': 4,
            'price_min': 1200,
            'price_max': 4000,
            'phone': '+90 252 555 0005',
            'email': 'info@bodrumblue.com',
            'amenities': [wifi, havuz, restoran, spa],
            'rooms': [
                {'name': 'Deniz Manzaralı Oda', 'price_per_night': 1200, 'capacity': 2, 'total_rooms': 25},
                {'name': 'Villa', 'price_per_night': 4000, 'capacity': 6, 'total_rooms': 5},
            ]
        },
    ]

    for data in hotels_data:
        if not Hotel.query.filter_by(name=data['name']).first():
            rooms = data.pop('rooms')
            amenities = data.pop('amenities')
            hotel = Hotel(owner_id=owner.id, is_approved=True, **data)
            hotel.amenities = [a for a in amenities if a]
            db.session.add(hotel)
            db.session.flush()

            for room_data in rooms:
                room = RoomType(hotel_id=hotel.id, **room_data)
                db.session.add(room)

    db.session.commit()
    print(f"Bitti: {len(hotels_data)} örnek otel eklendi.")


if __name__ == '__main__':
    with app.app_context():
        print("Basliyor: Seed data yukleniyor...")
        seed_amenities()
        admin = seed_admin()
        owner = seed_hotel_owner()
        seed_sample_user()
        seed_hotels(owner)
        print("\nBitti: Seed tamamlandi!")
        print("Giris bilgileri:")
        print("   Admin    -> admin@stayfinder.com / Admin123!")
        print("   Otelci   -> owner@stayfinder.com / Owner123!")
        print("   Kullanıcı-> user@stayfinder.com  / User123!")
