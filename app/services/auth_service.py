from typing import Tuple, Optional, Dict, Any
from app.models.user import User
from app.repositories.user_repository import UserRepository
from flask_login import login_user

class AuthService:
    """OTEL-8: Auth işlemleri için servis katmanı."""
    
    def __init__(self):
        self.user_repo = UserRepository()

    def register_user(self, data: Dict[str, Any]) -> Tuple[bool, str, Optional[User]]:
        """
        Kullanıcı kaydı yapar.
        Validasyon, şifre hashleme ve veritabanı kaydını gerçekleştirir.
        Dönüş: (success: bool, message: str, user: Optional[User])
        """
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'user')

        # Basit validasyonlar
        if not username or not email or not password:
            return False, "Tüm alanları doldurmak zorunludur.", None

        if self.user_repo.username_exists(username):
            return False, "Bu kullanıcı adı zaten alınmış.", None

        if self.user_repo.email_exists(email):
            return False, "Bu e-posta adresi ile zaten kayıt olunmuş.", None

        # Şifre kuralları
        if len(password) < 6:
            return False, "Şifre en az 6 karakter olmalıdır.", None

        # Yeni kullanıcı oluşturma
        new_user = User(
            username=username,
            email=email.lower(),
            role=role
        )
        new_user.set_password(password)

        try:
            self.user_repo.create(new_user)
            return True, "Kayıt başarıyla tamamlandı.", new_user
        except Exception as e:
            return False, f"Kayıt sırasında bir hata oluştu: {str(e)}", None

    def authenticate_user(self, email: str, password: str, remember: bool = False) -> Tuple[bool, str, Optional[User]]:
        """
        Kullanıcı girişi yapar (doğrulama).
        Dönüş: (success: bool, message: str, user: Optional[User])
        """
        user = self.user_repo.get_by_email(email)
        
        if not user:
            return False, "Bu e-posta adresi ile kayıtlı kullanıcı bulunamadı.", None
        
        if not user.check_password(password):
            return False, "Hatalı şifre girdiniz.", None

        if not user.is_active:
            return False, "Hesabınız pasif duruma getirilmiş.", None

        # Flask-Login ile oturum açma
        login_user(user, remember=remember)
        return True, "Başarıyla giriş yaptınız.", user
