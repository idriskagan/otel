from app.extensions import db

# Many-to-Many ilişki tablosu — Hotel ↔ Amenity
hotel_amenities = db.Table(
    'hotel_amenities',
    db.Column('hotel_id', db.Integer, db.ForeignKey('hotels.id'), primary_key=True),
    db.Column('amenity_id', db.Integer, db.ForeignKey('amenities.id'), primary_key=True)
)


class Amenity(db.Model):
    """Otel özellikleri modeli (WiFi, Havuz, SPA vb.)"""
    __tablename__ = 'amenities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    icon = db.Column(db.String(50), nullable=True)   # emoji veya icon class
    category = db.Column(db.String(50), nullable=True)  # genel, yiyecek, ulaşım vb.

    # İlişkiler
    hotels = db.relationship('Hotel', secondary=hotel_amenities, back_populates='amenities', lazy='subquery')

    def __repr__(self) -> str:
        return f'<Amenity {self.name}>'
