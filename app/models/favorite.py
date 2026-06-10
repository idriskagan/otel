from datetime import datetime
from app.extensions import db

class Favorite(db.Model):
    """OTEL-29.1: Kullanıcı favori (istek listesi) modeli."""
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Benzersiz kısıtlama: Bir kullanıcı bir oteli sadece bir kez favoriye alabilir.
    __table_args__ = (
        db.UniqueConstraint('user_id', 'hotel_id', name='uix_user_hotel_favorite'),
    )

    user = db.relationship('User', backref=db.backref('favorites', lazy='dynamic', cascade='all, delete-orphan'))
    hotel = db.relationship('Hotel', backref=db.backref('favorited_by', lazy='dynamic', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<Favorite User:{self.user_id} Hotel:{self.hotel_id}>'
