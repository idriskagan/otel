from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.utils.agent_debug import agent_debug_log


class User(UserMixin, db.Model):
    """Kullanıcı modeli — Presentation, Service ve Repository katmanları tarafından kullanılır."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')  # user | hotel_owner | admin
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # İlişkiler
    hotels = db.relationship('Hotel', back_populates='owner', lazy='dynamic')
    reservations = db.relationship('Reservation', back_populates='user', lazy='dynamic')
    reviews = db.relationship('Review', back_populates='user', lazy='dynamic')

    def set_password(self, password: str) -> None:
        """Şifreyi hash'leyerek kaydeder."""
        # region agent log
        agent_debug_log(
            run_id='register-debug',
            hypothesis_id='H2-H4',
            location='app/models/user.py:29',
            message='set_password called',
            data={
                'password_is_none': password is None,
                'password_length': len(password) if isinstance(password, str) else None,
            },
        )
        # endregion
        self.password_hash = generate_password_hash(password)
        # region agent log
        agent_debug_log(
            run_id='register-debug',
            hypothesis_id='H2-H4',
            location='app/models/user.py:41',
            message='set_password completed',
            data={
                'password_hash_is_none': self.password_hash is None,
                'password_hash_length': len(self.password_hash) if isinstance(self.password_hash, str) else None,
            },
        )
        # endregion

    def check_password(self, password: str) -> bool:
        """Verilen şifrenin hash ile uyuşup uyuşmadığını kontrol eder."""
        return check_password_hash(self.password_hash, password)

    def is_admin(self) -> bool:
        return self.role == 'admin'

    def is_hotel_owner(self) -> bool:
        return self.role == 'hotel_owner'

    def __repr__(self) -> str:
        return f'<User {self.username} ({self.role})>'
