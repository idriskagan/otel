from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.repositories.user_repository import UserRepository

class LoginForm(FlaskForm):
    """OTEL-9.1: Kullanıcı giriş formu."""
    email = StringField('E-posta', validators=[
        DataRequired(message="E-posta adresi zorunludur."),
        Email(message="Geçerli bir e-posta adresi giriniz.")
    ])
    password = PasswordField('Şifre', validators=[
        DataRequired(message="Şifre zorunludur.")
    ])
    remember = BooleanField('Beni Hatırla')
    submit = SubmitField('Giriş Yap')

class RegisterForm(FlaskForm):
    """OTEL-9.2: Kullanıcı kayıt formu."""
    username = StringField('Kullanıcı Adı', validators=[
        DataRequired(message="Kullanıcı adı zorunludur."),
        Length(min=3, max=20, message="Kullanıcı adı 3 ile 20 karakter arasında olmalıdır.")
    ])
    email = StringField('E-posta', validators=[
        DataRequired(message="E-posta adresi zorunludur."),
        Email(message="Geçerli bir e-posta adresi giriniz.")
    ])
    password = PasswordField('Şifre', validators=[
        DataRequired(message="Şifre zorunludur."),
        Length(min=6, message="Şifre en az 6 karakter olmalıdır.")
    ])
    confirm_password = PasswordField('Şifreyi Onayla', validators=[
        DataRequired(message="Şifre onayı zorunludur."),
        EqualTo('password', message="Şifreler eşleşmiyor.")
    ])
    role = SelectField('Kayıt Tipi', choices=[
        ('user', 'Misafir (Otel aramak ve rezervasyon yapmak istiyorum)'),
        ('hotel_owner', 'Otel Sahibi (Otelimi listelemek istiyorum)')
    ], default='user')
    submit = SubmitField('Kayıt Ol')

    def validate_username(self, field):
        repo = UserRepository()
        if repo.username_exists(field.data):
            raise ValidationError("Bu kullanıcı adı zaten kullanılıyor. Lütfen başka bir tane seçin.")

    def validate_email(self, field):
        repo = UserRepository()
        if repo.email_exists(field.data):
            raise ValidationError("Bu e-posta adresi zaten kullanımda. Giriş yapmayı deneyin.")
