from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, ValidationError
from flask_login import current_user
from app.repositories.user_repository import UserRepository


class ProfileUpdateForm(FlaskForm):
    """OTEL-28.1: Profil güncelleme formu (ad, soyad, telefon, bio, avatar)."""
    first_name = StringField('Ad', validators=[
        Optional(),
        Length(max=50, message="Ad en fazla 50 karakter olabilir.")
    ])
    last_name = StringField('Soyad', validators=[
        Optional(),
        Length(max=50, message="Soyad en fazla 50 karakter olabilir.")
    ])
    username = StringField('Kullanıcı Adı', validators=[
        DataRequired(message="Kullanıcı adı zorunludur."),
        Length(min=3, max=20, message="Kullanıcı adı 3 ile 20 karakter arasında olmalıdır.")
    ])
    email = StringField('E-posta', validators=[
        DataRequired(message="E-posta adresi zorunludur."),
        Email(message="Geçerli bir e-posta adresi giriniz.")
    ])
    phone = StringField('Telefon', validators=[
        Optional(),
        Length(max=20, message="Telefon numarası en fazla 20 karakter olabilir.")
    ])
    bio = TextAreaField('Hakkımda', validators=[
        Optional(),
        Length(max=500, message="Biyografi en fazla 500 karakter olabilir.")
    ])
    avatar = FileField('Profil Fotoğrafı', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Sadece JPG, PNG veya WebP dosyaları kabul edilir.')
    ])
    submit = SubmitField('Profili Güncelle')

    def validate_username(self, field):
        """Kullanıcı adı başkası tarafından kullanılıyor mu kontrol et."""
        repo = UserRepository()
        existing = repo.get_by_username(field.data)
        if existing and existing.id != current_user.id:
            raise ValidationError("Bu kullanıcı adı zaten kullanılıyor.")

    def validate_email(self, field):
        """E-posta başkası tarafından kullanılıyor mu kontrol et."""
        repo = UserRepository()
        existing = repo.get_by_email(field.data)
        if existing and existing.id != current_user.id:
            raise ValidationError("Bu e-posta adresi zaten kullanımda.")


class ChangePasswordForm(FlaskForm):
    """OTEL-28.6: Şifre değiştirme formu."""
    current_password = PasswordField('Mevcut Şifre', validators=[
        DataRequired(message="Mevcut şifrenizi girmeniz zorunludur.")
    ])
    new_password = PasswordField('Yeni Şifre', validators=[
        DataRequired(message="Yeni şifre zorunludur."),
        Length(min=6, message="Şifre en az 6 karakter olmalıdır.")
    ])
    confirm_password = PasswordField('Yeni Şifreyi Onayla', validators=[
        DataRequired(message="Şifre onayı zorunludur."),
        EqualTo('new_password', message="Yeni şifreler eşleşmiyor.")
    ])
    submit = SubmitField('Şifreyi Değiştir')
