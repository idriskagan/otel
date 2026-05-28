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
    
    # OTEL-31.3: Yorum yanıtlama ve düzenleme alanları
    parent_id = db.Column(db.Integer, db.ForeignKey('reviews.id'), nullable=True)
    is_edited = db.Column(db.Boolean, default=False, nullable=False)
    helpful_count = db.Column(db.Integer, default=0, nullable=False)

    # İlişkiler
    user = db.relationship('User', back_populates='reviews')
    hotel = db.relationship('Hotel', back_populates='reviews')
    replies = db.relationship('Review', backref=db.backref('parent', remote_side=[id]), lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f'<Review user={self.user_id} hotel={self.hotel_id} rating={self.rating}>'
