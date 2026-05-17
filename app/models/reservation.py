from datetime import datetime
from app.extensions import db


class Reservation(db.Model):
    """Rezervasyon modeli."""
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'), nullable=False, index=True)
    room_type_id = db.Column(db.Integer, db.ForeignKey('room_types.id'), nullable=False)
    check_in = db.Column(db.Date, nullable=False)
    check_out = db.Column(db.Date, nullable=False)
    guests = db.Column(db.Integer, nullable=False, default=1)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending | confirmed | cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # İlişkiler
    user = db.relationship('User', back_populates='reservations')
    hotel = db.relationship('Hotel', back_populates='reservations')
    room_type = db.relationship('RoomType', back_populates='reservations')

    @property
    def nights(self) -> int:
        """Rezervasyon süresini gece cinsinden döndürür."""
        return (self.check_out - self.check_in).days

    def __repr__(self) -> str:
        return f'<Reservation user={self.user_id} hotel={self.hotel_id} status={self.status}>'
