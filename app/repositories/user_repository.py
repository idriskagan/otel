from typing import List, Optional
from app.extensions import db
from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """OTEL-6.1: User entity için veri erişim katmanı."""

    def __init__(self):
        super().__init__(User)

    def get_by_email(self, email: str) -> Optional[User]:
        """Email'e göre kullanıcı döndürür."""
        return db.session.execute(
            db.select(User).where(User.email == email.lower())
        ).scalar_one_or_none()

    def get_by_username(self, username: str) -> Optional[User]:
        """Kullanıcı adına göre kullanıcı döndürür."""
        return db.session.execute(
            db.select(User).where(User.username == username)
        ).scalar_one_or_none()

    def get_by_role(self, role: str) -> List[User]:
        """Role göre kullanıcıları döndürür."""
        return db.session.execute(
            db.select(User).where(User.role == role)
        ).scalars().all()

    def email_exists(self, email: str) -> bool:
        """Email'in kullanılıp kullanılmadığını kontrol eder."""
        return self.get_by_email(email) is not None

    def username_exists(self, username: str) -> bool:
        """Kullanıcı adının kullanılıp kullanılmadığını kontrol eder."""
        return self.get_by_username(username) is not None

    def count_all(self) -> int:
        """Toplam kullanıcı sayısını döndürür."""
        return db.session.execute(db.select(db.func.count(User.id))).scalar()
