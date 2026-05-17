from datetime import datetime
from app.extensions import db
from app.models.amenity import hotel_amenities


class Hotel(db.Model):
    """Otel modeli."""
    __tablename__ = 'hotels'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(100), nullable=False, index=True)
    address = db.Column(db.String(300), nullable=True)
    star_rating = db.Column(db.Integer, nullable=False, default=3)  # 1-5
    price_min = db.Column(db.Float, nullable=True)
    price_max = db.Column(db.Float, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    is_approved = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # İlişkiler
    owner = db.relationship('User', back_populates='hotels')
    images = db.relationship('HotelImage', back_populates='hotel', lazy='dynamic', cascade='all, delete-orphan')
    room_types = db.relationship('RoomType', back_populates='hotel', lazy='dynamic', cascade='all, delete-orphan')
    reservations = db.relationship('Reservation', back_populates='hotel', lazy='dynamic')
    reviews = db.relationship('Review', back_populates='hotel', lazy='dynamic', cascade='all, delete-orphan')
    amenities = db.relationship('Amenity', secondary=hotel_amenities, back_populates='hotels', lazy='subquery')

    @property
    def primary_image(self):
        """Birincil otel fotoğrafını döndürür."""
        img = self.images.filter_by(is_primary=True).first()
        if img:
            return img.image_path
        first = self.images.first()
        return first.image_path if first else None

    @property
    def average_rating(self):
        """Ortalama yorum puanını döndürür."""
        reviews = self.reviews.all()
        if not reviews:
            return 0
        return round(sum(r.rating for r in reviews) / len(reviews), 1)

    @property
    def review_count(self):
        return self.reviews.count()

    def __repr__(self) -> str:
        return f'<Hotel {self.name} ({self.city})>'


class HotelImage(db.Model):
    """Otel fotoğraf modeli."""
    __tablename__ = 'hotel_images'

    id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'), nullable=False, index=True)
    image_path = db.Column(db.String(300), nullable=False)
    is_primary = db.Column(db.Boolean, default=False, nullable=False)
    sort_order = db.Column(db.Integer, default=0, nullable=False)

    # İlişkiler
    hotel = db.relationship('Hotel', back_populates='images')

    def __repr__(self) -> str:
        return f'<HotelImage hotel_id={self.hotel_id} primary={self.is_primary}>'
