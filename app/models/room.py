from app.extensions import db


class RoomType(db.Model):
    """Oda tipi modeli (Standart, Deluxe, Suite vb.)"""
    __tablename__ = 'room_types'

    id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price_per_night = db.Column(db.Float, nullable=False)
    capacity = db.Column(db.Integer, nullable=False, default=2)
    total_rooms = db.Column(db.Integer, nullable=False, default=1)

    # İlişkiler
    hotel = db.relationship('Hotel', back_populates='room_types')
    reservations = db.relationship('Reservation', back_populates='room_type', lazy='dynamic')

    def __repr__(self) -> str:
        return f'<RoomType {self.name} (Hotel ID: {self.hotel_id})>'
