from datetime import datetime
from app.extensions import db


class Review(db.Model):
    """Otel yorum modeli."""
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'), nullable=False, index=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # İlişkiler
    user = db.relationship('User', back_populates='reviews')
    hotel = db.relationship('Hotel', back_populates='reviews')

    def __repr__(self) -> str:
        return f'<Review user={self.user_id} hotel={self.hotel_id} rating={self.rating}>'
