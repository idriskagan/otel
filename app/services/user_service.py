import os
import uuid
from typing import Tuple, Optional
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask import current_app
from PIL import Image

from app.extensions import db
from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:
    """OTEL-28.3: Kullanıcı profil yönetimi için servis katmanı."""

    def __init__(self):
        self.user_repo = UserRepository()

    # ------------------------------------------------------------------
    # OTEL-28.3a: Profil güncelleme
    # ------------------------------------------------------------------
    def update_profile(
        self,
        user_id: int,
        data: dict,
        avatar_file: Optional[FileStorage] = None
    ) -> Tuple[bool, str]:
        """
        Kullanıcı profil bilgilerini günceller.
        Avatar dosyası varsa yeniden boyutlandırılarak kaydedilir.
        """
        user: Optional[User] = self.user_repo.get_by_id(user_id)
        if not user:
            return False, "Kullanıcı bulunamadı."

        try:
            # Metin alanlarını güncelle
            user.first_name = data.get('first_name', '').strip() or None
            user.last_name  = data.get('last_name', '').strip()  or None
            user.username   = data.get('username', user.username).strip()
            user.email      = data.get('email', user.email).strip().lower()
            user.phone      = data.get('phone', '').strip() or None
            user.bio        = data.get('bio', '').strip()   or None

            # Avatar yükleme
            if avatar_file and avatar_file.filename:
                avatar_path = self._save_avatar(user_id, avatar_file)
                if avatar_path:
                    # Eski avatarı sil
                    self._delete_old_avatar(user.avatar_path)
                    user.avatar_path = avatar_path

            db.session.commit()
            return True, "Profil başarıyla güncellendi."

        except Exception as e:
            db.session.rollback()
            return False, f"Profil güncellenirken hata oluştu: {str(e)}"

    # ------------------------------------------------------------------
    # OTEL-28.3b: Şifre değiştirme
    # ------------------------------------------------------------------
    def change_password(
        self,
        user_id: int,
        current_password: str,
        new_password: str
    ) -> Tuple[bool, str]:
        """
        Mevcut şifreyi doğrulayıp yeni şifre belirler.
        """
        user: Optional[User] = self.user_repo.get_by_id(user_id)
        if not user:
            return False, "Kullanıcı bulunamadı."

        if not user.check_password(current_password):
            return False, "Mevcut şifreniz hatalı."

        if len(new_password) < 6:
            return False, "Yeni şifre en az 6 karakter olmalıdır."

        try:
            user.set_password(new_password)
            db.session.commit()
            return True, "Şifreniz başarıyla değiştirildi."
        except Exception as e:
            db.session.rollback()
            return False, f"Şifre değiştirilirken hata oluştu: {str(e)}"

    # ------------------------------------------------------------------
    # Yardımcı metodlar
    # ------------------------------------------------------------------
    def _save_avatar(self, user_id: int, file: FileStorage) -> Optional[str]:
        """Avatar dosyasını kaydeder, 256×256 kırpar ve UUID ile adlandırır."""
        try:
            upload_folder = os.path.join(
                current_app.config.get('UPLOAD_FOLDER', 'app/static/uploads'),
                'avatars'
            )
            os.makedirs(upload_folder, exist_ok=True)

            ext = secure_filename(file.filename).rsplit('.', 1)[-1].lower()
            filename = f"avatar_{user_id}_{uuid.uuid4().hex[:8]}.{ext}"
            save_path = os.path.join(upload_folder, filename)

            img = Image.open(file.stream)
            img = img.convert('RGB')

            # Kare kırp (center crop)
            w, h = img.size
            side  = min(w, h)
            left  = (w - side) // 2
            top   = (h - side) // 2
            img   = img.crop((left, top, left + side, top + side))
            img   = img.resize((256, 256), Image.LANCZOS)
            img.save(save_path, quality=85, optimize=True)

            return filename
        except Exception:
            return None

    def _delete_old_avatar(self, avatar_path: Optional[str]) -> None:
        """Eski avatar dosyasını diskten siler."""
        if not avatar_path:
            return
        try:
            upload_folder = os.path.join(
                current_app.config.get('UPLOAD_FOLDER', 'app/static/uploads'),
                'avatars'
            )
            full_path = os.path.join(upload_folder, avatar_path)
            if os.path.exists(full_path):
                os.remove(full_path)
        except Exception:
            pass
