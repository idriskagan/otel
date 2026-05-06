from typing import Tuple, Optional
from flask_login import login_user, logout_user
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.utils.agent_debug import agent_debug_log


class AuthService:
    """OTEL-8: Authentication iş kuralları."""

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register_user(self, username: str, email: str, password: str, role: str = 'user') -> Tuple[bool, str]:
        """Yeni bir kullanıcı kaydeder ve durumu (başarı, mesaj) döner."""
        # region agent log
        agent_debug_log(
            run_id='register-debug',
            hypothesis_id='H1-H3',
            location='app/services/auth_service.py:15',
            message='register_user called',
            data={
                'username': username,
                'email': email,
                'role': role,
                'password_is_none': password is None,
                'password_length': len(password) if isinstance(password, str) else None,
            },
        )
        # endregion
        
        if self.user_repo.email_exists(email):
            return False, 'Bu e-posta adresi zaten kullanılıyor.'
        
        if self.user_repo.username_exists(username):
            return False, 'Bu kullanıcı adı zaten alınmış.'
            
        if role not in ['user', 'hotel_owner']:
            role = 'user'  # Güvenlik: Sadece user veya hotel_owner seçilebilir, admin seçilemez
            
        try:
            # Şifre hash'i flush/insert öncesi set edilmeli.
            # create() içinde flush olduğu için User nesnesini önce hazırlayıp save() ile yazıyoruz.
            # region agent log
            agent_debug_log(
                run_id='register-debug',
                hypothesis_id='H1',
                location='app/services/auth_service.py:39',
                message='before repository create',
                data={'username': username, 'email': email.lower(), 'role': role},
            )
            # endregion
            user = User(username=username, email=email.lower(), role=role)
            user.set_password(password)
            self.user_repo.save(user)
            self.user_repo.commit()
            return True, 'Kayıt başarılı! Lütfen giriş yapın.'
        except Exception as e:
            # region agent log
            agent_debug_log(
                run_id='register-debug',
                hypothesis_id='H1-H4',
                location='app/services/auth_service.py:53',
                message='register_user exception',
                data={'exception_type': type(e).__name__, 'exception': str(e)},
            )
            # endregion
            self.user_repo.rollback()
            return False, f'Kayıt sırasında bir hata oluştu: {str(e)}'

    def authenticate_and_login(self, email: str, password: str, remember: bool = False) -> Tuple[bool, str]:
        """Kullanıcıyı doğrular ve session başlatır."""
        user = self.user_repo.get_by_email(email)
        
        if not user or not user.check_password(password):
            return False, 'E-posta veya şifre hatalı.'
            
        if not user.is_active:
            return False, 'Hesabınız askıya alınmış.'
            
        # Flask-Login ile oturum aç
        login_user(user, remember=remember)
        return True, f'Hoş geldin, {user.username}!'

    def logout(self):
        """Kullanıcı oturumunu sonlandırır."""
        logout_user()